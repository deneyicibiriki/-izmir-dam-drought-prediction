"""
İzmir Baraj Veri Modeli - OOP Tabanlı Baraj Sınıfı
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field, validator

class DroughtLevel(Enum):
    """Kuraklık seviyesi enum"""
    NORMAL = "Normal"
    WARNING = "Dikkat"
    MODERATE = "Orta Kuraklık"
    SEVERE = "Şiddetli Kuraklık"
    CRITICAL = "Kritik Kuraklık"

class TrendDirection(Enum):
    """Trend yönü enum"""
    INCREASING = "Artış"
    DECREASING = "Azalış"
    STABLE = "Sabit"
    VOLATILE = "Değişken"

@dataclass
class DamLocation:
    """Baraj konum bilgileri"""
    latitude: float
    longitude: float
    district: str
    water_source: str
    
    def __post_init__(self):
        """Koordinat validasyonu"""
        if not (-90 <= self.latitude <= 90):
            raise ValueError(f"Geçersiz enlem: {self.latitude}")
        if not (-180 <= self.longitude <= 180):
            raise ValueError(f"Geçersiz boylam: {self.longitude}")

@dataclass
class DamCapacity:
    """Baraj kapasite bilgileri"""
    total_capacity_mcm: float
    current_volume_mcm: float
    fill_ratio: float
    
    def __post_init__(self):
        """Kapasite validasyonu"""
        if self.total_capacity_mcm <= 0:
            raise ValueError("Toplam kapasite pozitif olmalıdır")
        if self.current_volume_mcm < 0:
            raise ValueError("Mevcut hacim negatif olamaz")
        if self.current_volume_mcm > self.total_capacity_mcm:
            raise ValueError("Mevcut hacim toplam kapasiteyi aşamaz")
        
        # Doluluk oranını hesapla
        self.fill_ratio = self.current_volume_mcm / self.total_capacity_mcm

class DamData(BaseModel):
    """Baraj veri modeli - Pydantic ile validasyon"""
    
    dam_name: str = Field(..., description="Baraj adı")
    date: datetime = Field(..., description="Veri tarihi")
    current_volume_mcm: float = Field(..., ge=0, description="Mevcut hacim (mcm)")
    total_capacity_mcm: float = Field(..., gt=0, description="Toplam kapasite (mcm)")
    fill_ratio: float = Field(..., ge=0, le=1, description="Doluluk oranı")
    inflow_mcm: Optional[float] = Field(None, ge=0, description="Giriş debisi (mcm)")
    outflow_mcm: Optional[float] = Field(None, ge=0, description="Çıkış debisi (mcm)")
    evaporation_mcm: Optional[float] = Field(None, ge=0, description="Buharlaşma (mcm)")
    
    @validator('fill_ratio')
    def validate_fill_ratio(cls, v, values):
        """Doluluk oranı validasyonu"""
        if 'current_volume_mcm' in values and 'total_capacity_mcm' in values:
            expected_ratio = values['current_volume_mcm'] / values['total_capacity_mcm']
            if abs(v - expected_ratio) > 0.01:  # %1 tolerans
                raise ValueError(f"Doluluk oranı hesaplanan değerle uyuşmuyor: {v} vs {expected_ratio}")
        return v

class Dam:
    """İzmir Baraj Sınıfı - Ana baraj modeli"""
    
    def __init__(self, name: str, location: DamLocation, capacity: DamCapacity):
        """
        Baraj sınıfı başlatıcı
        
        Args:
            name: Baraj adı
            location: Baraj konumu
            capacity: Baraj kapasitesi
        """
        self.name = name
        self.location = location
        self.capacity = capacity
        self.historical_data: List[DamData] = []
        self.weather_data: List[Dict] = []
        
    def add_historical_data(self, data: DamData) -> None:
        """Geçmiş veri ekle"""
        self.historical_data.append(data)
        # Tarihe göre sırala
        self.historical_data.sort(key=lambda x: x.date)
    
    def add_weather_data(self, weather_data: Dict) -> None:
        """Meteorolojik veri ekle"""
        self.weather_data.append(weather_data)
    
    def get_current_status(self) -> Optional[DamData]:
        """Mevcut durumu döndür"""
        if not self.historical_data:
            return None
        return self.historical_data[-1]
    
    def get_drought_level(self) -> DroughtLevel:
        """Kuraklık seviyesini belirle"""
        current_data = self.get_current_status()
        if not current_data:
            return DroughtLevel.NORMAL
        
        fill_ratio = current_data.fill_ratio
        
        if fill_ratio >= 0.8:
            return DroughtLevel.NORMAL
        elif fill_ratio >= 0.6:
            return DroughtLevel.WARNING
        elif fill_ratio >= 0.4:
            return DroughtLevel.MODERATE
        elif fill_ratio >= 0.2:
            return DroughtLevel.SEVERE
        else:
            return DroughtLevel.CRITICAL
    
    def calculate_trend(self, days: int = 30) -> TrendDirection:
        """Trend analizi yap"""
        if len(self.historical_data) < 2:
            return TrendDirection.STABLE
        
        # Son N günün verilerini al
        recent_data = [d for d in self.historical_data 
                      if d.date >= datetime.now() - timedelta(days=days)]
        
        if len(recent_data) < 2:
            return TrendDirection.STABLE
        
        # Lineer regresyon ile trend hesapla
        x = np.arange(len(recent_data))
        y = [d.fill_ratio for d in recent_data]
        
        slope = np.polyfit(x, y, 1)[0]
        
        # Volatilite kontrolü
        volatility = np.std(y)
        
        if volatility > 0.1:  # %10'dan fazla volatilite
            return TrendDirection.VOLATILE
        elif slope > 0.01:  # %1'den fazla artış
            return TrendDirection.INCREASING
        elif slope < -0.01:  # %1'den fazla azalış
            return TrendDirection.DECREASING
        else:
            return TrendDirection.STABLE
    
    def get_water_balance(self, days: int = 7) -> Dict:
        """Su dengesi hesapla"""
        recent_data = [d for d in self.historical_data 
                      if d.date >= datetime.now() - timedelta(days=days)]
        
        if len(recent_data) < 2:
            return {"error": "Yetersiz veri"}
        
        total_inflow = sum(d.inflow_mcm or 0 for d in recent_data)
        total_outflow = sum(d.outflow_mcm or 0 for d in recent_data)
        total_evaporation = sum(d.evaporation_mcm or 0 for d in recent_data)
        
        net_change = total_inflow - total_outflow - total_evaporation
        
        return {
            "total_inflow": total_inflow,
            "total_outflow": total_outflow,
            "total_evaporation": total_evaporation,
            "net_change": net_change,
            "period_days": days
        }
    
    def predict_water_level(self, days_ahead: int, weather_forecast: List[Dict] = None) -> List[Dict]:
        """Su seviyesi tahmini"""
        if not self.historical_data:
            return []
        
        predictions = []
        current_data = self.get_current_status()
        
        if not current_data:
            return []
        
        # Basit trend bazlı tahmin
        trend = self.calculate_trend()
        current_volume = current_data.current_volume_mcm
        
        for day in range(1, days_ahead + 1):
            # Trend faktörü
            if trend == TrendDirection.INCREASING:
                volume_change = 0.5  # günlük artış
            elif trend == TrendDirection.DECREASING:
                volume_change = -0.5  # günlük azalış
            else:
                volume_change = 0.0  # sabit
            
            # Hava durumu faktörü
            if weather_forecast and day <= len(weather_forecast):
                weather = weather_forecast[day - 1]
                precipitation = weather.get('precipitation', 0)
                temperature = weather.get('temperature', 20)
                
                # Yağış faktörü
                if precipitation > 5:  # 5mm'den fazla yağış
                    volume_change += precipitation * 0.1
                
                # Sıcaklık faktörü (buharlaşma)
                if temperature > 25:
                    volume_change -= (temperature - 25) * 0.02
            
            # Yeni hacim hesapla
            new_volume = max(0, min(current_volume + volume_change, self.capacity.total_capacity_mcm))
            new_fill_ratio = new_volume / self.capacity.total_capacity_mcm
            
            predictions.append({
                "date": (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d"),
                "predicted_volume_mcm": round(new_volume, 2),
                "predicted_fill_ratio": round(new_fill_ratio, 3),
                "drought_level": self._get_drought_level_from_ratio(new_fill_ratio)
            })
            
            current_volume = new_volume
        
        return predictions
    
    def _get_drought_level_from_ratio(self, fill_ratio: float) -> str:
        """Doluluk oranından kuraklık seviyesi belirle"""
        if fill_ratio >= 0.8:
            return DroughtLevel.NORMAL.value
        elif fill_ratio >= 0.6:
            return DroughtLevel.WARNING.value
        elif fill_ratio >= 0.4:
            return DroughtLevel.MODERATE.value
        elif fill_ratio >= 0.2:
            return DroughtLevel.SEVERE.value
        else:
            return DroughtLevel.CRITICAL.value
    
    def to_dataframe(self) -> pd.DataFrame:
        """Baraj verilerini DataFrame'e çevir"""
        if not self.historical_data:
            return pd.DataFrame()
        
        data = []
        for dam_data in self.historical_data:
            data.append({
                "dam_name": self.name,
                "date": dam_data.date,
                "current_volume_mcm": dam_data.current_volume_mcm,
                "total_capacity_mcm": dam_data.total_capacity_mcm,
                "fill_ratio": dam_data.fill_ratio,
                "inflow_mcm": dam_data.inflow_mcm,
                "outflow_mcm": dam_data.outflow_mcm,
                "evaporation_mcm": dam_data.evaporation_mcm,
                "latitude": self.location.latitude,
                "longitude": self.location.longitude,
                "district": self.location.district,
                "water_source": self.location.water_source
            })
        
        return pd.DataFrame(data)
    
    def get_summary(self) -> Dict:
        """Baraj özet bilgileri"""
        current_data = self.get_current_status()
        if not current_data:
            return {"error": "Veri bulunamadı"}
        
        return {
            "name": self.name,
            "location": {
                "latitude": self.location.latitude,
                "longitude": self.location.longitude,
                "district": self.location.district,
                "water_source": self.location.water_source
            },
            "capacity": {
                "total_capacity_mcm": self.capacity.total_capacity_mcm,
                "current_volume_mcm": current_data.current_volume_mcm,
                "fill_ratio": current_data.fill_ratio
            },
            "status": {
                "drought_level": self.get_drought_level().value,
                "trend": self.calculate_trend().value,
                "data_points": len(self.historical_data)
            }
        }

class DamManager:
    """Baraj yönetici sınıfı - Birden fazla barajı yönetir"""
    
    def __init__(self):
        self.dams: Dict[str, Dam] = {}
    
    def add_dam(self, dam: Dam) -> None:
        """Baraj ekle"""
        self.dams[dam.name] = dam
    
    def get_dam(self, name: str) -> Optional[Dam]:
        """Baraj getir"""
        return self.dams.get(name)
    
    def get_all_dams(self) -> List[Dam]:
        """Tüm barajları getir"""
        return list(self.dams.values())
    
    def get_dams_by_district(self, district: str) -> List[Dam]:
        """İlçeye göre barajları getir"""
        return [dam for dam in self.dams.values() 
                if dam.location.district == district]
    
    def get_critical_dams(self) -> List[Dam]:
        """Kritik seviyedeki barajları getir"""
        return [dam for dam in self.dams.values() 
                if dam.get_drought_level() in [DroughtLevel.SEVERE, DroughtLevel.CRITICAL]]
    
    def get_overall_status(self) -> Dict:
        """Genel durum raporu"""
        total_dams = len(self.dams)
        if total_dams == 0:
            return {"error": "Baraj bulunamadı"}
        
        drought_counts = {level.value: 0 for level in DroughtLevel}
        
        for dam in self.dams.values():
            drought_level = dam.get_drought_level()
            drought_counts[drought_level.value] += 1
        
        return {
            "total_dams": total_dams,
            "drought_distribution": drought_counts,
            "critical_dams": len(self.get_critical_dams()),
            "average_fill_ratio": np.mean([dam.get_current_status().fill_ratio 
                                         for dam in self.dams.values() 
                                         if dam.get_current_status()])
        }

