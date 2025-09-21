"""
İzmir Baraj Doluluk ve Kuraklık Riski Tahmini - Ana Uygulama
OOP Tabanlı, API ve CSV Veri Kaynakları Desteği
"""
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

# Proje modüllerini import et
from config.settings import settings
from models.dam import Dam, DamLocation, DamCapacity, DamData, DamManager, DroughtLevel
from services.data_service import DataService, IZSUAPIService, WeatherAPIService, CSVDataSource
from services.weather_service import WeatherService

# Logging ayarları
logging.basicConfig(
    level=getattr(logging, settings.logging.log_level),
    format=settings.logging.log_format,
    handlers=[
        logging.FileHandler(settings.logging.log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class IzmirDamPredictionApp:
    """İzmir Baraj Doluluk ve Kuraklık Riski Tahmini Ana Uygulama Sınıfı"""
    
    def __init__(self):
        """Uygulama başlatıcı"""
        self.data_service = DataService()
        self.weather_service = WeatherService()
        self.dam_manager = DamManager()
        
        # Veri depolama
        self.dam_data: pd.DataFrame = pd.DataFrame()
        self.weather_data: pd.DataFrame = pd.DataFrame()
        self.combined_data: pd.DataFrame = pd.DataFrame()
        self.predictions: pd.DataFrame = pd.DataFrame()
        
        logger.info("İzmir Baraj Doluluk ve Kuraklık Riski Tahmini uygulaması başlatıldı")
    
    def setup_data_sources(self, dam_source: str = "csv", weather_source: str = "csv", **kwargs):
        """
        Veri kaynaklarını ayarla
        
        Args:
            dam_source: Baraj veri kaynağı ("api" veya "csv")
            weather_source: Meteorolojik veri kaynağı ("api" veya "csv")
            **kwargs: Ek parametreler (file_path, api_type vb.)
        """
        logger.info(f"Veri kaynakları ayarlanıyor - Baraj: {dam_source}, Hava: {weather_source}")
        
        # Baraj veri kaynağını ayarla
        if dam_source == "api":
            self.data_service.set_dam_data_source("api")
        elif dam_source == "csv":
            file_path = kwargs.get('dam_csv_path', settings.data.csv_dam_data_path)
            self.data_service.set_dam_data_source("csv", file_path=file_path)
        else:
            raise ValueError(f"Desteklenmeyen baraj veri kaynağı: {dam_source}")
        
        # Meteorolojik veri kaynağını ayarla
        if weather_source == "api":
            api_type = kwargs.get('weather_api_type', 'meteo')
            self.data_service.set_weather_data_source("api", api_type=api_type)
        elif weather_source == "csv":
            file_path = kwargs.get('weather_csv_path', settings.data.csv_weather_data_path)
            self.data_service.set_weather_data_source("csv", file_path=file_path)
        else:
            raise ValueError(f"Desteklenmeyen meteorolojik veri kaynağı: {weather_source}")
        
        logger.info("Veri kaynakları başarıyla ayarlandı")
    
    def load_dam_data(self, dam_names: List[str] = None, days: int = 30) -> bool:
        """
        Baraj verilerini yükle
        
        Args:
            dam_names: Yüklenecek baraj isimleri (None ise tümü)
            days: Kaç günlük veri
        
        Returns:
            bool: Yükleme başarılı mı
        """
        try:
            logger.info("Baraj verileri yükleniyor...")
            
            if dam_names is None:
                dam_names = settings.get_all_dam_names()
            
            # Veri çek
            self.dam_data = self.data_service.fetch_dam_data(
                dam_names=dam_names,
                days=days
            )
            
            if self.dam_data.empty:
                logger.warning("Baraj verisi yüklenemedi")
                return False
            
            # DamManager'a barajları ekle
            self._populate_dam_manager()
            
            logger.info(f"Baraj verileri yüklendi: {len(self.dam_data)} kayıt")
            return True
            
        except Exception as e:
            logger.error(f"Baraj veri yükleme hatası: {e}")
            return False
    
    def load_weather_data(self, dam_names: List[str] = None, days: int = 30) -> bool:
        """
        Meteorolojik verileri yükle
        
        Args:
            dam_names: Hava durumu alınacak baraj isimleri
            days: Kaç günlük veri
        
        Returns:
            bool: Yükleme başarılı mı
        """
        try:
            logger.info("Meteorolojik veriler yükleniyor...")
            
            if dam_names is None:
                dam_names = settings.get_all_dam_names()
            
            weather_data_list = []
            
            for dam_name in dam_names:
                # Her baraj için meteorolojik veri çek
                dam_weather = self.weather_service.get_weather_for_dam(dam_name, days)
                if not dam_weather.empty:
                    weather_data_list.append(dam_weather)
            
            if weather_data_list:
                self.weather_data = pd.concat(weather_data_list, ignore_index=True)
                logger.info(f"Meteorolojik veriler yüklendi: {len(self.weather_data)} kayıt")
                return True
            else:
                logger.warning("Meteorolojik veri yüklenemedi")
                return False
                
        except Exception as e:
            logger.error(f"Meteorolojik veri yükleme hatası: {e}")
            return False
    
    def _populate_dam_manager(self) -> None:
        """DamManager'ı baraj verileriyle doldur"""
        if self.dam_data.empty:
            return
        
        # Her baraj için Dam objesi oluştur
        for dam_name in self.dam_data['dam_name'].unique():
            dam_info = settings.get_dam_info(dam_name)
            if not dam_info:
                continue
            
            # Konum bilgisi
            location = DamLocation(
                latitude=dam_info['latitude'],
                longitude=dam_info['longitude'],
                district=dam_info['district'],
                water_source=dam_info['water_source']
            )
            
            # Kapasite bilgisi
            capacity = DamCapacity(
                total_capacity_mcm=dam_info['capacity_mcm'],
                current_volume_mcm=0,  # Güncellenecek
                fill_ratio=0.0
            )
            
            # Dam objesi oluştur
            dam = Dam(dam_name, location, capacity)
            
            # Geçmiş verileri ekle
            dam_data = self.dam_data[self.dam_data['dam_name'] == dam_name]
            for _, row in dam_data.iterrows():
                dam_data_obj = DamData(
                    dam_name=row['dam_name'],
                    date=pd.to_datetime(row['date']),
                    current_volume_mcm=row['current_volume_mcm'],
                    total_capacity_mcm=row['total_capacity_mcm'],
                    fill_ratio=row['fill_ratio'],
                    inflow_mcm=row.get('inflow_mcm'),
                    outflow_mcm=row.get('outflow_mcm'),
                    evaporation_mcm=row.get('evaporation_mcm')
                )
                dam.add_historical_data(dam_data_obj)
            
            # DamManager'a ekle
            self.dam_manager.add_dam(dam)
    
    def process_data(self) -> bool:
        """Verileri işle ve birleştir"""
        try:
            logger.info("Veriler işleniyor ve birleştiriliyor...")
            
            if self.dam_data.empty or self.weather_data.empty:
                logger.warning("İşlenecek veri yok")
                return False
            
            # Verileri birleştir
            self.combined_data = pd.merge(
                self.dam_data,
                self.weather_data,
                on=['date', 'dam_name'],
                how='inner'
            )
            
            if self.combined_data.empty:
                logger.warning("Veri birleştirme başarısız")
                return False
            
            logger.info(f"Veri işleme tamamlandı: {len(self.combined_data)} kayıt")
            return True
            
        except Exception as e:
            logger.error(f"Veri işleme hatası: {e}")
            return False
    
    def analyze_dams(self) -> Dict:
        """Baraj analizi yap"""
        logger.info("Baraj analizi yapılıyor...")
        
        analysis_results = {}
        
        for dam in self.dam_manager.get_all_dams():
            dam_analysis = {
                "current_status": dam.get_current_status(),
                "drought_level": dam.get_drought_level().value,
                "trend": dam.calculate_trend().value,
                "water_balance": dam.get_water_balance(),
                "summary": dam.get_summary()
            }
            analysis_results[dam.name] = dam_analysis
        
        # Genel durum
        overall_status = self.dam_manager.get_overall_status()
        analysis_results["overall_status"] = overall_status
        
        return analysis_results
    
    def predict_future_levels(self, days_ahead: int = None) -> Dict:
        """
        Gelecek su seviyelerini tahmin et
        
        Args:
            days_ahead: Kaç gün ileriye tahmin
        
        Returns:
            Dict: Tahmin sonuçları
        """
        if days_ahead is None:
            days_ahead = settings.model.prediction_days
        
        logger.info(f"{days_ahead} günlük tahmin yapılıyor...")
        
        predictions = {}
        
        for dam in self.dam_manager.get_all_dams():
            # Basit trend bazlı tahmin
            dam_predictions = dam.predict_water_level(days_ahead)
            predictions[dam.name] = dam_predictions
        
        self.predictions = predictions
        return predictions
    
    def generate_alerts(self) -> List[Dict]:
        """Uyarılar oluştur"""
        alerts = []
        
        for dam in self.dam_manager.get_all_dams():
            current_data = dam.get_current_status()
            if not current_data:
                continue
            
            drought_level = dam.get_drought_level()
            
            # Kritik seviye uyarıları
            if drought_level == DroughtLevel.CRITICAL:
                alerts.append({
                    "type": "CRITICAL",
                    "dam_name": dam.name,
                    "message": f"{dam.name} barajı kritik seviyede! Doluluk oranı: {current_data.fill_ratio:.1%}",
                    "severity": "high",
                    "date": current_data.date.strftime('%Y-%m-%d')
                })
            elif drought_level == DroughtLevel.SEVERE:
                alerts.append({
                    "type": "SEVERE_DROUGHT",
                    "dam_name": dam.name,
                    "message": f"{dam.name} barajında şiddetli kuraklık! Doluluk oranı: {current_data.fill_ratio:.1%}",
                    "severity": "medium",
                    "date": current_data.date.strftime('%Y-%m-%d')
                })
            
            # Trend uyarıları
            trend = dam.calculate_trend()
            if trend.value == "Azalış":
                alerts.append({
                    "type": "DECLINING_TREND",
                    "dam_name": dam.name,
                    "message": f"{dam.name} barajında düşüş trendi tespit edildi",
                    "severity": "low",
                    "date": current_data.date.strftime('%Y-%m-%d')
                })
        
        return alerts
    
    def generate_report(self) -> Dict:
        """Kapsamlı analiz raporu oluştur"""
        logger.info("Analiz raporu oluşturuluyor...")
        
        # Baraj analizi
        dam_analysis = self.analyze_dams()
        
        # Tahminler
        predictions = self.predict_future_levels()
        
        # Uyarılar
        alerts = self.generate_alerts()
        
        # Veri kalitesi
        data_quality = self._assess_data_quality()
        
        # Meteorolojik veri özeti
        weather_summary = {}
        if not self.weather_data.empty:
            weather_summary = self.weather_service.get_weather_summary(self.weather_data)
        
        report = {
            "report_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "data_sources": self.data_service.get_data_summary(),
            "dam_analysis": dam_analysis,
            "predictions": predictions,
            "alerts": alerts,
            "data_quality": data_quality,
            "weather_summary": weather_summary,
            "settings": {
                "prediction_days": settings.model.prediction_days,
                "drought_threshold": settings.model.drought_threshold,
                "critical_threshold": settings.model.critical_threshold
            }
        }
        
        return report
    
    def _assess_data_quality(self) -> Dict:
        """Veri kalitesini değerlendir"""
        if self.combined_data.empty:
            return {"score": 0, "issues": ["Veri yok"]}
        
        issues = []
        score = 100
        
        # Eksik değer kontrolü
        missing_ratio = self.combined_data.isnull().sum().sum() / (len(self.combined_data) * len(self.combined_data.columns))
        if missing_ratio > settings.data.max_missing_ratio:
            issues.append(f"Yüksek eksik veri oranı: {missing_ratio:.1%}")
            score -= 20
        
        # Veri tutarlılığı
        if 'fill_ratio' in self.combined_data.columns:
            invalid_ratios = (self.combined_data['fill_ratio'] < 0) | (self.combined_data['fill_ratio'] > 1)
            if invalid_ratios.any():
                issues.append(f"Geçersiz doluluk oranları: {invalid_ratios.sum()} kayıt")
                score -= 15
        
        # Veri boyutu
        if len(self.combined_data) < settings.data.min_data_points:
            issues.append("Yetersiz veri boyutu")
            score -= 25
        
        return {
            "score": max(score, 0),
            "issues": issues,
            "total_records": len(self.combined_data),
            "missing_ratio": missing_ratio
        }
    
    def save_results(self, output_dir: str = "results") -> None:
        """Sonuçları dosyaya kaydet"""
        import os
        import json
        
        # Çıktı dizinini oluştur
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Verileri kaydet
        if not self.combined_data.empty:
            self.combined_data.to_csv(f'{output_dir}/izmir_combined_data_{timestamp}.csv', index=False)
        
        if self.predictions:
            # Tahminleri DataFrame'e çevir ve kaydet
            pred_data = []
            for dam_name, preds in self.predictions.items():
                for pred in preds:
                    pred['dam_name'] = dam_name
                    pred_data.append(pred)
            
            if pred_data:
                pred_df = pd.DataFrame(pred_data)
                pred_df.to_csv(f'{output_dir}/izmir_predictions_{timestamp}.csv', index=False)
        
        # Raporu kaydet
        report = self.generate_report()
        with open(f'{output_dir}/izmir_report_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"Sonuçlar kaydedildi: {output_dir}")

def main():
    """Ana fonksiyon"""
    print("=== İzmir Baraj Doluluk ve Kuraklık Riski Tahmini ===")
    print()
    
    # Uygulamayı başlat
    app = IzmirDamPredictionApp()
    
    # Kullanıcıdan veri kaynağı seçimi al
    print("Veri kaynağı seçin:")
    print("1. CSV dosyalarından oku")
    print("2. API'lerden çek")
    
    choice = input("Seçiminiz (1 veya 2): ").strip()
    
    if choice == "1":
        print("CSV dosyalarından veri yükleniyor...")
        app.setup_data_sources(dam_source="csv", weather_source="csv")
    elif choice == "2":
        print("API'lerden veri çekiliyor...")
        app.setup_data_sources(dam_source="api", weather_source="api")
    else:
        print("Geçersiz seçim, CSV dosyaları kullanılıyor...")
        app.setup_data_sources(dam_source="csv", weather_source="csv")
    
    # Verileri yükle
    print("1. Baraj verileri yükleniyor...")
    if not app.load_dam_data():
        print("Baraj verileri yüklenemedi!")
        return
    
    print("2. Meteorolojik veriler yükleniyor...")
    if not app.load_weather_data():
        print("Meteorolojik veriler yüklenemedi!")
        return
    
    # Verileri işle
    print("3. Veriler işleniyor...")
    if not app.process_data():
        print("Veri işleme başarısız!")
        return
    
    # Analiz yap
    print("4. Baraj analizi yapılıyor...")
    analysis = app.analyze_dams()
    
    # Tahmin yap
    print("5. Gelecek tahminleri yapılıyor...")
    predictions = app.predict_future_levels()
    
    # Rapor oluştur
    print("6. Analiz raporu oluşturuluyor...")
    report = app.generate_report()
    
    # Sonuçları göster
    print("\n=== ANALİZ SONUÇLARI ===")
    
    overall_status = analysis.get("overall_status", {})
    print(f"Toplam Baraj Sayısı: {overall_status.get('total_dams', 0)}")
    print(f"Ortalama Doluluk Oranı: {overall_status.get('average_fill_ratio', 0):.1%}")
    print(f"Kritik Seviyedeki Barajlar: {overall_status.get('critical_dams', 0)}")
    
    # Kuraklık dağılımı
    drought_dist = overall_status.get('drought_distribution', {})
    print(f"\nKuraklık Dağılımı:")
    for level, count in drought_dist.items():
        print(f"  {level}: {count} baraj")
    
    # Uyarılar
    alerts = report.get('alerts', [])
    if alerts:
        print(f"\nUyarılar ({len(alerts)}):")
        for alert in alerts:
            print(f"  - {alert['message']}")
    
    # Veri kalitesi
    data_quality = report.get('data_quality', {})
    print(f"\nVeri Kalitesi: {data_quality.get('score', 0)}/100")
    
    # Sonuçları kaydet
    print("\n7. Sonuçlar kaydediliyor...")
    app.save_results()
    
    print("\nAnaliz tamamlandı! Sonuçlar 'results' klasöründe kaydedildi.")

if __name__ == "__main__":
    main()

