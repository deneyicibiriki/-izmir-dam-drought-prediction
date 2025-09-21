"""
Veri Servisi - API ve CSV veri kaynakları için OOP tabanlı servis sınıfları
"""
import pandas as pd
import requests
import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Any
from datetime import datetime, timedelta
import logging
from pathlib import Path
import time
from config.settings import settings

logger = logging.getLogger(__name__)

class DataSource(ABC):
    """Veri kaynağı için abstract base class"""
    
    @abstractmethod
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """Veri çekme metodu - alt sınıflarda implement edilmeli"""
        pass
    
    @abstractmethod
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Veri validasyonu - alt sınıflarda implement edilmeli"""
        pass

class APIDataSource(DataSource):
    """API veri kaynağı sınıfı"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'IzmirDamPrediction/1.0',
            'Content-Type': 'application/json'
        })
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def _make_request(self, endpoint: str, params: Dict = None, retries: int = None) -> Dict:
        """API isteği yap"""
        if retries is None:
            retries = settings.api.max_retries
        
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(retries + 1):
            try:
                response = self.session.get(
                    url, 
                    params=params, 
                    timeout=settings.api.api_timeout
                )
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"API isteği başarısız (deneme {attempt + 1}/{retries + 1}): {e}")
                if attempt < retries:
                    time.sleep(settings.api.retry_delay * (2 ** attempt))  # Exponential backoff
                else:
                    logger.error(f"API isteği tamamen başarısız: {url}")
                    raise
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """API verisi validasyonu"""
        if data.empty:
            logger.warning("API'den boş veri döndü")
            return False
        
        required_columns = ['date', 'dam_name', 'fill_ratio']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            logger.error(f"Eksik sütunlar: {missing_columns}")
            return False
        
        # Veri kalitesi kontrolü
        if data['fill_ratio'].isna().sum() > len(data) * settings.data.max_missing_ratio:
            logger.warning("Çok fazla eksik veri")
            return False
        
        return True

class IZSUAPIService(APIDataSource):
    """İZSU API servisi"""
    
    def __init__(self):
        super().__init__(
            base_url=settings.api.izsu_base_url,
            api_key=settings.api.izsu_api_key
        )
    
    def fetch_dam_data(self, dam_names: List[str] = None, 
                      start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """İZSU'dan baraj verilerini çek"""
        try:
            params = {}
            if dam_names:
                params['dam_names'] = ','.join(dam_names)
            if start_date:
                params['start_date'] = start_date
            if end_date:
                params['end_date'] = end_date
            
            data = self._make_request(settings.api.izsu_dam_data_endpoint, params)
            
            if not data or 'results' not in data:
                logger.warning("İZSU API'den veri döndürülmedi")
                return pd.DataFrame()
            
            # Veriyi DataFrame'e çevir
            df = pd.DataFrame(data['results'])
            
            # Tarih sütununu datetime'a çevir
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            
            logger.info(f"İZSU API'den {len(df)} kayıt çekildi")
            return df
            
        except Exception as e:
            logger.error(f"İZSU API veri çekme hatası: {e}")
            return pd.DataFrame()
    
    def fetch_water_levels(self, dam_name: str, days: int = 30) -> pd.DataFrame:
        """Su seviyesi verilerini çek"""
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            params = {
                'dam_name': dam_name,
                'start_date': start_date,
                'end_date': end_date
            }
            
            data = self._make_request(settings.api.izsu_water_level_endpoint, params)
            
            if not data or 'results' not in data:
                return pd.DataFrame()
            
            df = pd.DataFrame(data['results'])
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            
            return df
            
        except Exception as e:
            logger.error(f"Su seviyesi veri çekme hatası: {e}")
            return pd.DataFrame()
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """Genel veri çekme metodu"""
        return self.fetch_dam_data(**kwargs)

class WeatherAPIService(APIDataSource):
    """Meteorolojik veri API servisi"""
    
    def __init__(self, api_type: str = "openweather"):
        self.api_type = api_type
        
        if api_type == "openweather":
            super().__init__(
                base_url=settings.api.openweather_base_url,
                api_key=settings.api.openweather_api_key
            )
        elif api_type == "meteo":
            super().__init__(base_url=settings.api.meteo_base_url)
        else:
            raise ValueError(f"Desteklenmeyen API tipi: {api_type}")
    
    def fetch_weather_data(self, latitude: float, longitude: float, 
                          days: int = 30) -> pd.DataFrame:
        """Meteorolojik veri çek"""
        try:
            if self.api_type == "openweather":
                return self._fetch_openweather_data(latitude, longitude, days)
            elif self.api_type == "meteo":
                return self._fetch_meteo_data(latitude, longitude, days)
        except Exception as e:
            logger.error(f"Meteorolojik veri çekme hatası: {e}")
            return pd.DataFrame()
    
    def _fetch_openweather_data(self, lat: float, lon: float, days: int) -> pd.DataFrame:
        """OpenWeather API'den veri çek"""
        # Geçmiş veri için One Call API
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',
            'exclude': 'minutely,alerts'
        }
        
        data = self._make_request('/onecall', params)
        
        if not data or 'daily' not in data:
            return pd.DataFrame()
        
        records = []
        for day_data in data['daily'][:days]:
            record = {
                'date': datetime.fromtimestamp(day_data['dt']).strftime('%Y-%m-%d'),
                'temp_max': day_data['temp']['max'],
                'temp_min': day_data['temp']['min'],
                'precipitation': day_data.get('rain', {}).get('1h', 0) + 
                               day_data.get('snow', {}).get('1h', 0),
                'humidity': day_data['humidity'],
                'pressure': day_data['pressure'],
                'wind_speed': day_data['wind_speed'],
                'latitude': lat,
                'longitude': lon
            }
            records.append(record)
        
        return pd.DataFrame(records)
    
    def _fetch_meteo_data(self, lat: float, lon: float, days: int) -> pd.DataFrame:
        """Open-Meteo API'den veri çek"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_hours',
            'timezone': 'Europe/Istanbul',
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }
        
        data = self._make_request('/forecast', params)
        
        if not data or 'daily' not in data:
            return pd.DataFrame()
        
        records = []
        daily_data = data['daily']
        for i in range(len(daily_data['time'])):
            record = {
                'date': daily_data['time'][i],
                'temp_max': daily_data['temperature_2m_max'][i],
                'temp_min': daily_data['temperature_2m_min'][i],
                'precipitation': daily_data['precipitation_sum'][i],
                'precipitation_hours': daily_data['precipitation_hours'][i],
                'latitude': lat,
                'longitude': lon
            }
            records.append(record)
        
        return pd.DataFrame(records)
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """Genel veri çekme metodu"""
        return self.fetch_weather_data(**kwargs)
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Meteorolojik veri validasyonu"""
        if data.empty:
            return False
        
        required_columns = ['date', 'temp_max', 'temp_min', 'precipitation']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            logger.error(f"Eksik meteorolojik veri sütunları: {missing_columns}")
            return False
        
        return True

class CSVDataSource(DataSource):
    """CSV veri kaynağı sınıfı"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"CSV dosyası bulunamadı: {file_path}")
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """CSV dosyasından veri oku"""
        try:
            # Dosya uzantısına göre okuma yöntemi seç
            if self.file_path.suffix.lower() == '.csv':
                df = pd.read_csv(self.file_path)
            elif self.file_path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(self.file_path)
            else:
                raise ValueError(f"Desteklenmeyen dosya formatı: {self.file_path.suffix}")
            
            # Tarih sütununu datetime'a çevir
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            
            logger.info(f"CSV dosyasından {len(df)} kayıt okundu: {self.file_path}")
            return df
            
        except Exception as e:
            logger.error(f"CSV okuma hatası: {e}")
            return pd.DataFrame()
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """CSV veri validasyonu"""
        if data.empty:
            logger.warning("CSV dosyası boş")
            return False
        
        # Minimum veri noktası kontrolü
        if len(data) < settings.data.min_data_points:
            logger.warning(f"Yetersiz veri noktası: {len(data)} < {settings.data.min_data_points}")
            return False
        
        return True

class DataService:
    """Ana veri servisi - Tüm veri kaynaklarını yönetir"""
    
    def __init__(self):
        self.dam_data_source: Optional[DataSource] = None
        self.weather_data_source: Optional[DataSource] = None
        self.cache: Dict[str, pd.DataFrame] = {}
        self.cache_timestamps: Dict[str, datetime] = {}
    
    def set_dam_data_source(self, source_type: str, **kwargs) -> None:
        """Baraj veri kaynağını ayarla"""
        if source_type == "api":
            self.dam_data_source = IZSUAPIService()
        elif source_type == "csv":
            file_path = kwargs.get('file_path', settings.data.csv_dam_data_path)
            self.dam_data_source = CSVDataSource(file_path)
        else:
            raise ValueError(f"Desteklenmeyen veri kaynağı: {source_type}")
    
    def set_weather_data_source(self, source_type: str, **kwargs) -> None:
        """Meteorolojik veri kaynağını ayarla"""
        if source_type == "api":
            api_type = kwargs.get('api_type', 'openweather')
            self.weather_data_source = WeatherAPIService(api_type)
        elif source_type == "csv":
            file_path = kwargs.get('file_path', settings.data.csv_weather_data_path)
            self.weather_data_source = CSVDataSource(file_path)
        else:
            raise ValueError(f"Desteklenmeyen veri kaynağı: {source_type}")
    
    def fetch_dam_data(self, **kwargs) -> pd.DataFrame:
        """Baraj verilerini çek"""
        if not self.dam_data_source:
            raise ValueError("Baraj veri kaynağı ayarlanmamış")
        
        # Cache kontrolü
        cache_key = f"dam_data_{hash(str(kwargs))}"
        if self._is_cache_valid(cache_key):
            logger.info("Baraj verisi cache'den döndürülüyor")
            return self.cache[cache_key]
        
        # Veri çek
        data = self.dam_data_source.fetch_data(**kwargs)
        
        # Validasyon
        if self.dam_data_source.validate_data(data):
            self._update_cache(cache_key, data)
            return data
        else:
            logger.error("Baraj verisi validasyonu başarısız")
            return pd.DataFrame()
    
    def fetch_weather_data(self, **kwargs) -> pd.DataFrame:
        """Meteorolojik verileri çek"""
        if not self.weather_data_source:
            raise ValueError("Meteorolojik veri kaynağı ayarlanmamış")
        
        # Cache kontrolü
        cache_key = f"weather_data_{hash(str(kwargs))}"
        if self._is_cache_valid(cache_key):
            logger.info("Meteorolojik veri cache'den döndürülüyor")
            return self.cache[cache_key]
        
        # Veri çek
        data = self.weather_data_source.fetch_data(**kwargs)
        
        # Validasyon
        if self.weather_data_source.validate_data(data):
            self._update_cache(cache_key, data)
            return data
        else:
            logger.error("Meteorolojik veri validasyonu başarısız")
            return pd.DataFrame()
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Cache geçerliliğini kontrol et"""
        if cache_key not in self.cache:
            return False
        
        cache_time = self.cache_timestamps.get(cache_key)
        if not cache_time:
            return False
        
        return (datetime.now() - cache_time).seconds < settings.data.cache_duration
    
    def _update_cache(self, cache_key: str, data: pd.DataFrame) -> None:
        """Cache'i güncelle"""
        self.cache[cache_key] = data.copy()
        self.cache_timestamps[cache_key] = datetime.now()
    
    def clear_cache(self) -> None:
        """Cache'i temizle"""
        self.cache.clear()
        self.cache_timestamps.clear()
        logger.info("Cache temizlendi")
    
    def get_data_summary(self) -> Dict:
        """Veri özeti"""
        summary = {
            "dam_data_source": type(self.dam_data_source).__name__ if self.dam_data_source else None,
            "weather_data_source": type(self.weather_data_source).__name__ if self.weather_data_source else None,
            "cache_size": len(self.cache),
            "cache_keys": list(self.cache.keys())
        }
        return summary

