"""
Hava Durumu API Servisi - Open-Meteo ve MGM API'lerinden meteorolojik veri çekme
"""
import pandas as pd
import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
import time
from config.settings import settings

logger = logging.getLogger(__name__)

class WeatherAPIService:
    """Hava durumu API servisleri"""
    
    def __init__(self):
        self.meteo_base_url = settings.api.meteo_base_url
        self.mgm_base_url = settings.api.mgm_base_url
        self.openweather_base_url = settings.api.openweather_base_url
        self.openweather_api_key = settings.api.openweather_api_key
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'IzmirDamPrediction/1.0',
            'Accept': 'application/json'
        })
    
    def fetch_weather_data(self, dam_names: List[str], days: int = 30) -> pd.DataFrame:
        """
        Hava durumu verilerini çek
        
        Args:
            dam_names: Baraj isimleri
            days: Kaç günlük veri
            
        Returns:
            pd.DataFrame: Hava durumu verileri
        """
        try:
            logger.info("Hava durumu verileri çekiliyor...")
            
            # Önce Open-Meteo'yu dene (ücretsiz)
            weather_data = self._fetch_from_open_meteo(dam_names, days)
            
            if weather_data.empty:
                # MGM'yi dene
                weather_data = self._fetch_from_mgm(dam_names, days)
            
            if weather_data.empty:
                # OpenWeather'ı dene (API anahtarı gerekli)
                weather_data = self._fetch_from_openweather(dam_names, days)
            
            if weather_data.empty:
                logger.warning("Hava durumu verisi çekilemedi, örnek veri kullanılıyor")
                weather_data = self._create_sample_weather_data(dam_names, days)
            
            logger.info(f"{len(weather_data)} hava durumu kaydı çekildi")
            return weather_data
            
        except Exception as e:
            logger.error(f"Hava durumu veri çekme hatası: {e}")
            return self._create_sample_weather_data(dam_names, days)
    
    def _fetch_from_open_meteo(self, dam_names: List[str], days: int) -> pd.DataFrame:
        """
        Open-Meteo API'den veri çek (ücretsiz)
        
        Args:
            dam_names: Baraj isimleri
            days: Kaç günlük veri
            
        Returns:
            pd.DataFrame: Hava durumu verileri
        """
        try:
            weather_data = []
            
            for dam_name in dam_names:
                dam_info = settings.get_dam_info(dam_name)
                if not dam_info:
                    continue
                
                latitude = dam_info['latitude']
                longitude = dam_info['longitude']
                
                # Geçmiş veri için
                start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
                end_date = datetime.now().strftime('%Y-%m-%d')
                
                # Open-Meteo API parametreleri
                params = {
                    'latitude': latitude,
                    'longitude': longitude,
                    'start_date': start_date,
                    'end_date': end_date,
                    'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_mean,pressure_msl_mean,wind_speed_10m_max',
                    'timezone': 'Europe/Istanbul'
                }
                
                url = f"{self.meteo_base_url}{settings.api.meteo_historical_endpoint}"
                response = self.session.get(url, params=params, timeout=settings.api.api_timeout)
                response.raise_for_status()
                
                data = response.json()
                
                if 'daily' in data:
                    daily_data = data['daily']
                    dates = daily_data['time']
                    
                    for i, date in enumerate(dates):
                        weather_data.append({
                            'date': date,
                            'dam_name': dam_name,
                            'temp_max': daily_data['temperature_2m_max'][i],
                            'temp_min': daily_data['temperature_2m_min'][i],
                            'precipitation': daily_data['precipitation_sum'][i],
                            'humidity': daily_data['relative_humidity_2m_mean'][i],
                            'pressure': daily_data['pressure_msl_mean'][i],
                            'wind_speed': daily_data['wind_speed_10m_max'][i],
                            'latitude': latitude,
                            'longitude': longitude,
                            'nearest_station': f"Open-Meteo_{dam_name}"
                        })
                
                # API rate limiting
                time.sleep(0.1)
            
            return pd.DataFrame(weather_data)
            
        except Exception as e:
            logger.error(f"Open-Meteo API hatası: {e}")
            return pd.DataFrame()
    
    def _fetch_from_mgm(self, dam_names: List[str], days: int) -> pd.DataFrame:
        """
        MGM (Türkiye Meteoroloji Genel Müdürlüğü) API'den veri çek
        
        Args:
            dam_names: Baraj isimleri
            days: Kaç günlük veri
            
        Returns:
            pd.DataFrame: Hava durumu verileri
        """
        try:
            weather_data = []
            
            # MGM API endpoint'i
            url = f"{self.mgm_base_url}{settings.api.mgm_weather_endpoint}"
            
            # İzmir için istasyon ID'si (örnek)
            izmir_station_id = "17200"  # İzmir merkez istasyonu
            
            params = {
                'istno': izmir_station_id,
                'gunluk': '1'
            }
            
            response = self.session.get(url, params=params, timeout=settings.api.api_timeout)
            response.raise_for_status()
            
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                for record in data:
                    date_str = record.get('tarih', '')
                    if date_str:
                        # Tüm barajlar için aynı hava durumu verisi kullan
                        for dam_name in dam_names:
                            weather_data.append({
                                'date': date_str,
                                'dam_name': dam_name,
                                'temp_max': record.get('mak', 0),
                                'temp_min': record.get('min', 0),
                                'precipitation': record.get('yagis', 0),
                                'humidity': record.get('nem', 0),
                                'pressure': record.get('basinc', 0),
                                'wind_speed': record.get('ruzgar', 0),
                                'latitude': 38.4192,  # İzmir merkez
                                'longitude': 27.1287,
                                'nearest_station': 'MGM_İzmir'
                            })
            
            return pd.DataFrame(weather_data)
            
        except Exception as e:
            logger.error(f"MGM API hatası: {e}")
            return pd.DataFrame()
    
    def _fetch_from_openweather(self, dam_names: List[str], days: int) -> pd.DataFrame:
        """
        OpenWeather API'den veri çek (API anahtarı gerekli)
        
        Args:
            dam_names: Baraj isimleri
            days: Kaç günlük veri
            
        Returns:
            pd.DataFrame: Hava durumu verileri
        """
        if not self.openweather_api_key:
            logger.warning("OpenWeather API anahtarı bulunamadı")
            return pd.DataFrame()
        
        try:
            weather_data = []
            
            for dam_name in dam_names:
                dam_info = settings.get_dam_info(dam_name)
                if not dam_info:
                    continue
                
                latitude = dam_info['latitude']
                longitude = dam_info['longitude']
                
                # OpenWeather One Call API
                url = f"{self.openweather_base_url}/onecall"
                params = {
                    'lat': latitude,
                    'lon': longitude,
                    'appid': self.openweather_api_key,
                    'units': 'metric',
                    'exclude': 'minutely,alerts'
                }
                
                response = self.session.get(url, params=params, timeout=settings.api.api_timeout)
                response.raise_for_status()
                
                data = response.json()
                
                if 'daily' in data:
                    for daily in data['daily'][:days]:
                        date = datetime.fromtimestamp(daily['dt']).strftime('%Y-%m-%d')
                        
                        weather_data.append({
                            'date': date,
                            'dam_name': dam_name,
                            'temp_max': daily['temp']['max'],
                            'temp_min': daily['temp']['min'],
                            'precipitation': daily.get('rain', {}).get('1h', 0) + daily.get('snow', {}).get('1h', 0),
                            'humidity': daily['humidity'],
                            'pressure': daily['pressure'],
                            'wind_speed': daily['wind_speed'],
                            'latitude': latitude,
                            'longitude': longitude,
                            'nearest_station': f"OpenWeather_{dam_name}"
                        })
                
                # API rate limiting
                time.sleep(0.1)
            
            return pd.DataFrame(weather_data)
            
        except Exception as e:
            logger.error(f"OpenWeather API hatası: {e}")
            return pd.DataFrame()
    
    def _create_sample_weather_data(self, dam_names: List[str], days: int) -> pd.DataFrame:
        """
        Örnek hava durumu verisi oluştur
        
        Args:
            dam_names: Baraj isimleri
            days: Kaç günlük veri
            
        Returns:
            pd.DataFrame: Örnek hava durumu verileri
        """
        import numpy as np
        
        weather_data = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            for dam_name in dam_names:
                dam_info = settings.get_dam_info(dam_name)
                if not dam_info:
                    continue
                
                # Gerçekçi hava durumu verileri
                weather_data.append({
                    'date': date,
                    'dam_name': dam_name,
                    'temp_max': np.random.uniform(15, 35),
                    'temp_min': np.random.uniform(5, 20),
                    'precipitation': np.random.exponential(2.0),
                    'humidity': np.random.uniform(40, 80),
                    'pressure': np.random.uniform(1000, 1020),
                    'wind_speed': np.random.uniform(5, 15),
                    'latitude': dam_info['latitude'],
                    'longitude': dam_info['longitude'],
                    'nearest_station': f"Sample_{dam_name}"
                })
        
        return pd.DataFrame(weather_data)
    
    def get_current_weather(self, dam_name: str) -> Optional[Dict]:
        """
        Belirli bir baraj için güncel hava durumu
        
        Args:
            dam_name: Baraj adı
            
        Returns:
            Dict: Güncel hava durumu
        """
        try:
            weather_data = self.fetch_weather_data([dam_name], days=1)
            
            if weather_data.empty:
                return None
            
            latest = weather_data.iloc[-1]
            return {
                'dam_name': dam_name,
                'date': latest['date'],
                'temperature': (latest['temp_max'] + latest['temp_min']) / 2,
                'precipitation': latest['precipitation'],
                'humidity': latest['humidity'],
                'pressure': latest['pressure'],
                'wind_speed': latest['wind_speed'],
                'station': latest['nearest_station']
            }
            
        except Exception as e:
            logger.error(f"Güncel hava durumu çekme hatası: {e}")
            return None
    
    def get_weather_forecast(self, dam_name: str, days: int = 7) -> pd.DataFrame:
        """
        Hava durumu tahmini
        
        Args:
            dam_name: Baraj adı
            days: Kaç günlük tahmin
            
        Returns:
            pd.DataFrame: Hava durumu tahmini
        """
        try:
            # Open-Meteo tahmin API'si
            dam_info = settings.get_dam_info(dam_name)
            if not dam_info:
                return pd.DataFrame()
            
            latitude = dam_info['latitude']
            longitude = dam_info['longitude']
            
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_mean,pressure_msl_mean,wind_speed_10m_max',
                'forecast_days': days,
                'timezone': 'Europe/Istanbul'
            }
            
            url = f"{self.meteo_base_url}{settings.api.meteo_forecast_endpoint}"
            response = self.session.get(url, params=params, timeout=settings.api.api_timeout)
            response.raise_for_status()
            
            data = response.json()
            
            forecast_data = []
            if 'daily' in data:
                daily_data = data['daily']
                dates = daily_data['time']
                
                for i, date in enumerate(dates):
                    forecast_data.append({
                        'date': date,
                        'dam_name': dam_name,
                        'temp_max': daily_data['temperature_2m_max'][i],
                        'temp_min': daily_data['temperature_2m_min'][i],
                        'precipitation': daily_data['precipitation_sum'][i],
                        'humidity': daily_data['relative_humidity_2m_mean'][i],
                        'pressure': daily_data['pressure_msl_mean'][i],
                        'wind_speed': daily_data['wind_speed_10m_max'][i],
                        'latitude': latitude,
                        'longitude': longitude,
                        'nearest_station': f"Forecast_{dam_name}"
                    })
            
            return pd.DataFrame(forecast_data)
            
        except Exception as e:
            logger.error(f"Hava durumu tahmini hatası: {e}")
            return pd.DataFrame()
