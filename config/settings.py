"""
İzmir Baraj Doluluk ve Kuraklık Riski Tahmini - Konfigürasyon Ayarları
"""
import os
from typing import Dict, List, Optional
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()

class APIConfig(BaseSettings):
    """API konfigürasyon sınıfı"""
    
    # İZSU Web Servis API Ayarları (Gerçek URL'ler)
    izsu_base_url: str = Field(
        default="https://www.izsu.gov.tr",
        description="İZSU web sitesi temel URL'i"
    )
    izsu_dam_data_endpoint: str = Field(
        default="/tr/baraj-doluluk-oranlari",
        description="Baraj doluluk oranları sayfası"
    )
    izsu_water_level_endpoint: str = Field(
        default="/tr/su-seviyeleri",
        description="Su seviyeleri sayfası"
    )
    izsu_api_endpoint: str = Field(
        default="/api/dam-data",
        description="İZSU API endpoint'i (eğer varsa)"
    )
    izsu_api_key: Optional[str] = Field(
        default=None,
        description="İZSU API anahtarı"
    )
    
    # Meteorolojik Veri API'leri
    openweather_api_key: Optional[str] = Field(
        default=None,
        description="OpenWeather API anahtarı"
    )
    openweather_base_url: str = Field(
        default="https://api.openweathermap.org/data/2.5",
        description="OpenWeather API temel URL'i"
    )
    
    # Open-Meteo API (Ücretsiz, API anahtarı gerektirmez)
    meteo_base_url: str = Field(
        default="https://api.open-meteo.com/v1",
        description="Open-Meteo API temel URL'i"
    )
    meteo_forecast_endpoint: str = Field(
        default="/forecast",
        description="Open-Meteo tahmin endpoint'i"
    )
    meteo_historical_endpoint: str = Field(
        default="/forecast",
        description="Open-Meteo geçmiş veri endpoint'i"
    )
    
    # Türkiye Meteoroloji Genel Müdürlüğü API
    mgm_base_url: str = Field(
        default="https://servis.mgm.gov.tr",
        description="MGM API temel URL'i"
    )
    mgm_weather_endpoint: str = Field(
        default="/web/sondurumlar",
        description="MGM hava durumu endpoint'i"
    )
    
    # API Timeout ve Retry Ayarları
    api_timeout: int = Field(default=30, description="API timeout süresi (saniye)")
    max_retries: int = Field(default=3, description="Maksimum retry sayısı")
    retry_delay: int = Field(default=1, description="Retry arası bekleme süresi (saniye)")

class DataConfig(BaseSettings):
    """Veri konfigürasyon sınıfı"""
    
    # Veri Kaynakları
    data_sources: List[str] = Field(
        default=["api", "csv"],
        description="Desteklenen veri kaynakları"
    )
    
    # CSV Dosya Yolları
    csv_dam_data_path: str = Field(
        default="data/izmir_dam_data.csv",
        description="Baraj verileri CSV dosya yolu"
    )
    csv_weather_data_path: str = Field(
        default="data/izmir_weather_data.csv",
        description="Meteorolojik veriler CSV dosya yolu"
    )
    
    # Veri Kalitesi Ayarları
    min_data_points: int = Field(default=30, description="Minimum veri noktası sayısı")
    max_missing_ratio: float = Field(default=0.2, description="Maksimum eksik veri oranı")
    
    # Veri Güncelleme Ayarları
    data_update_interval: int = Field(default=3600, description="Veri güncelleme aralığı (saniye)")
    cache_duration: int = Field(default=1800, description="Cache süresi (saniye)")

class ModelConfig(BaseSettings):
    """Model konfigürasyon sınıfı"""
    
    # Tahmin Parametreleri
    prediction_days: int = Field(default=30, description="Tahmin gün sayısı")
    drought_threshold: float = Field(default=0.3, description="Kuraklık eşik değeri")
    critical_threshold: float = Field(default=0.1, description="Kritik seviye eşik değeri")
    
    # Model Parametreleri
    model_types: List[str] = Field(
        default=["random_forest", "gradient_boosting", "logistic_regression"],
        description="Kullanılacak model tipleri"
    )
    cross_validation_folds: int = Field(default=5, description="Cross-validation fold sayısı")
    test_size: float = Field(default=0.2, description="Test set oranı")
    
    # Özellik Mühendisliği
    lag_features: List[int] = Field(
        default=[1, 3, 7, 14, 30],
        description="Lag özellik günleri"
    )
    moving_average_windows: List[int] = Field(
        default=[7, 14, 30],
        description="Hareketli ortalama pencereleri"
    )

class VisualizationConfig(BaseSettings):
    """Görselleştirme konfigürasyon sınıfı"""
    
    # Harita Ayarları
    map_center: List[float] = Field(
        default=[38.4192, 27.1287],  # İzmir merkezi
        description="Harita merkez koordinatları"
    )
    map_zoom: int = Field(default=9, description="Harita zoom seviyesi")
    
    # Renk Paleti
    colors: Dict[str, str] = Field(
        default={
            "normal": "#2E8B57",
            "warning": "#FFD700", 
            "critical": "#FF4500",
            "drought": "#8B0000",
            "background": "#F5F5F5"
        },
        description="Görselleştirme renkleri"
    )
    
    # Grafik Ayarları
    figure_size: tuple = Field(default=(12, 8), description="Grafik boyutu")
    dpi: int = Field(default=300, description="Grafik çözünürlüğü")

class LoggingConfig(BaseSettings):
    """Logging konfigürasyon sınıfı"""
    
    log_level: str = Field(default="INFO", description="Log seviyesi")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log formatı"
    )
    log_file: str = Field(default="logs/izmir_dam_prediction.log", description="Log dosya yolu")

class Settings:
    """Ana konfigürasyon sınıfı"""
    
    def __init__(self):
        self.api = APIConfig()
        self.data = DataConfig()
        self.model = ModelConfig()
        self.visualization = VisualizationConfig()
        self.logging = LoggingConfig()
        
        # İzmir Barajları Bilgileri
        self.izmir_dams = self._get_izmir_dams()
    
    def _get_izmir_dams(self) -> Dict:
        """İzmir bölgesi barajları bilgileri"""
        return {
            "Tahtalı": {
                "name": "Tahtalı Barajı",
                "latitude": 38.3167,
                "longitude": 27.1500,
                "capacity_mcm": 150.0,
                "district": "Konak",
                "water_source": "Tahtalı Deresi"
            },
            "Balçova": {
                "name": "Balçova Barajı", 
                "latitude": 38.3833,
                "longitude": 27.0167,
                "capacity_mcm": 25.0,
                "district": "Balçova",
                "water_source": "Balçova Deresi"
            },
            "Güzelhisar": {
                "name": "Güzelhisar Barajı",
                "latitude": 38.2500,
                "longitude": 27.1000,
                "capacity_mcm": 45.0,
                "district": "Aliağa",
                "water_source": "Güzelhisar Deresi"
            },
            "Çamlı": {
                "name": "Çamlı Barajı",
                "latitude": 38.4500,
                "longitude": 27.2000,
                "capacity_mcm": 35.0,
                "district": "Bornova",
                "water_source": "Çamlı Deresi"
            },
            "Gediz": {
                "name": "Gediz Barajı",
                "latitude": 38.5000,
                "longitude": 27.3000,
                "capacity_mcm": 80.0,
                "district": "Menemen",
                "water_source": "Gediz Nehri"
            }
        }
    
    def get_dam_info(self, dam_name: str) -> Optional[Dict]:
        """Belirli bir barajın bilgilerini döndürür"""
        return self.izmir_dams.get(dam_name)
    
    def get_all_dam_names(self) -> List[str]:
        """Tüm baraj isimlerini döndürür"""
        return list(self.izmir_dams.keys())
    
    def get_dam_coordinates(self, dam_name: str) -> Optional[tuple]:
        """Baraj koordinatlarını döndürür"""
        dam_info = self.get_dam_info(dam_name)
        if dam_info:
            return (dam_info["latitude"], dam_info["longitude"])
        return None

# Global settings instance
settings = Settings()

