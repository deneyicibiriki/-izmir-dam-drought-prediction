"""
Meteorolojik Veri Servisi - İzmir bölgesi için özelleştirilmiş
"""
import pandas as pd
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from geopy.distance import geodesic
import numpy as np
from config.settings import settings

logger = logging.getLogger(__name__)

class WeatherStation:
    """Meteoroloji istasyonu sınıfı"""
    
    def __init__(self, station_id: str, name: str, latitude: float, longitude: float):
        self.station_id = station_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.data: List[Dict] = []
    
    def add_weather_data(self, weather_data: Dict) -> None:
        """Meteorolojik veri ekle"""
        self.data.append(weather_data)
    
    def get_distance_to_point(self, lat: float, lon: float) -> float:
        """Belirli bir noktaya olan mesafeyi hesapla (km)"""
        return geodesic((self.latitude, self.longitude), (lat, lon)).kilometers

class WeatherService:
    """İzmir bölgesi meteorolojik veri servisi"""
    
    def __init__(self):
        self.weather_stations: Dict[str, WeatherStation] = {}
        self._initialize_izmir_stations()
    
    def _initialize_izmir_stations(self) -> None:
        """İzmir bölgesi meteoroloji istasyonlarını başlat"""
        # İzmir ve çevresindeki meteoroloji istasyonları
        stations_data = [
            {
                "station_id": "IZMIR_001",
                "name": "İzmir Merkez",
                "latitude": 38.4192,
                "longitude": 27.1287
            },
            {
                "station_id": "IZMIR_002", 
                "name": "Çeşme",
                "latitude": 38.3167,
                "longitude": 26.3000
            },
            {
                "station_id": "IZMIR_003",
                "name": "Bergama",
                "latitude": 39.1167,
                "longitude": 27.1833
            },
            {
                "station_id": "IZMIR_004",
                "name": "Menemen",
                "latitude": 38.6000,
                "longitude": 27.0667
            },
            {
                "station_id": "IZMIR_005",
                "name": "Tire",
                "latitude": 38.0833,
                "longitude": 27.7333
            },
            {
                "station_id": "IZMIR_006",
                "name": "Ödemiş",
                "latitude": 38.2167,
                "longitude": 27.9667
            },
            {
                "station_id": "IZMIR_007",
                "name": "Aliağa",
                "latitude": 38.8000,
                "longitude": 26.9667
            },
            {
                "station_id": "IZMIR_008",
                "name": "Bornova",
                "latitude": 38.4500,
                "longitude": 27.2000
            }
        ]
        
        for station_data in stations_data:
            station = WeatherStation(
                station_id=station_data["station_id"],
                name=station_data["name"],
                latitude=station_data["latitude"],
                longitude=station_data["longitude"]
            )
            self.weather_stations[station.station_id] = station
    
    def get_nearest_station(self, latitude: float, longitude: float, 
                          max_distance_km: float = 50.0) -> Optional[WeatherStation]:
        """En yakın meteoroloji istasyonunu bul"""
        nearest_station = None
        min_distance = float('inf')
        
        for station in self.weather_stations.values():
            distance = station.get_distance_to_point(latitude, longitude)
            if distance < min_distance and distance <= max_distance_km:
                min_distance = distance
                nearest_station = station
        
        return nearest_station
    
    def fetch_weather_for_location(self, latitude: float, longitude: float, 
                                 days: int = 30, api_type: str = "meteo") -> pd.DataFrame:
        """Belirli konum için meteorolojik veri çek"""
        try:
            if api_type == "meteo":
                return self._fetch_meteo_weather(latitude, longitude, days)
            elif api_type == "openweather":
                return self._fetch_openweather_data(latitude, longitude, days)
            else:
                raise ValueError(f"Desteklenmeyen API tipi: {api_type}")
        except Exception as e:
            logger.error(f"Meteorolojik veri çekme hatası: {e}")
            return pd.DataFrame()
    
    def _fetch_meteo_weather(self, lat: float, lon: float, days: int) -> pd.DataFrame:
        """Open-Meteo API'den veri çek"""
        base_url = settings.api.meteo_base_url
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_hours,relative_humidity_2m,pressure_msl,wind_speed_10m_max',
            'timezone': 'Europe/Istanbul',
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }
        
        try:
            response = requests.get(f"{base_url}/forecast", params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'daily' not in data:
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
                    'humidity': daily_data['relative_humidity_2m'][i],
                    'pressure': daily_data['pressure_msl'][i],
                    'wind_speed': daily_data['wind_speed_10m_max'][i],
                    'latitude': lat,
                    'longitude': lon
                }
                records.append(record)
            
            df = pd.DataFrame(records)
            logger.info(f"Open-Meteo'dan {len(df)} günlük meteorolojik veri çekildi")
            return df
            
        except Exception as e:
            logger.error(f"Open-Meteo API hatası: {e}")
            return pd.DataFrame()
    
    def _fetch_openweather_data(self, lat: float, lon: float, days: int) -> pd.DataFrame:
        """OpenWeather API'den veri çek"""
        api_key = settings.api.openweather_api_key
        if not api_key:
            logger.warning("OpenWeather API anahtarı bulunamadı")
            return pd.DataFrame()
        
        base_url = settings.api.openweather_base_url
        
        # Geçmiş veri için One Call API
        params = {
            'lat': lat,
            'lon': lon,
            'appid': api_key,
            'units': 'metric',
            'exclude': 'minutely,alerts'
        }
        
        try:
            response = requests.get(f"{base_url}/onecall", params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'daily' not in data:
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
            
            df = pd.DataFrame(records)
            logger.info(f"OpenWeather'dan {len(df)} günlük meteorolojik veri çekildi")
            return df
            
        except Exception as e:
            logger.error(f"OpenWeather API hatası: {e}")
            return pd.DataFrame()
    
    def get_weather_for_dam(self, dam_name: str, days: int = 30) -> pd.DataFrame:
        """Baraj için meteorolojik veri çek"""
        dam_info = settings.get_dam_info(dam_name)
        if not dam_info:
            logger.error(f"Baraj bilgisi bulunamadı: {dam_name}")
            return pd.DataFrame()
        
        latitude = dam_info['latitude']
        longitude = dam_info['longitude']
        
        # En yakın istasyonu bul
        nearest_station = self.get_nearest_station(latitude, longitude)
        if nearest_station:
            logger.info(f"{dam_name} barajı için en yakın istasyon: {nearest_station.name}")
        
        # Meteorolojik veri çek
        weather_data = self.fetch_weather_for_location(latitude, longitude, days)
        
        if not weather_data.empty:
            weather_data['dam_name'] = dam_name
            weather_data['nearest_station'] = nearest_station.name if nearest_station else "Unknown"
        
        return weather_data
    
    def create_sample_weather_data(self, dam_name: str, days: int = 365) -> pd.DataFrame:
        """Örnek meteorolojik veri oluştur (test amaçlı)"""
        dam_info = settings.get_dam_info(dam_name)
        if not dam_info:
            logger.error(f"Baraj bilgisi bulunamadı: {dam_name}")
            return pd.DataFrame()
        
        dates = pd.date_range(start=datetime.now() - timedelta(days=days), 
                            end=datetime.now(), freq='D')
        
        # İzmir iklimine uygun mevsimsel değişim
        seasonal_temp = 18 + 8 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
        seasonal_precip = 1.5 + 2 * np.sin(2 * np.pi * (np.arange(len(dates)) + 90) / 365.25)
        
        data = {
            'date': dates.strftime('%Y-%m-%d'),
            'temp_max': seasonal_temp + np.random.normal(0, 3, len(dates)),
            'temp_min': seasonal_temp - 8 + np.random.normal(0, 2, len(dates)),
            'precipitation': np.maximum(0, seasonal_precip + np.random.normal(0, 2, len(dates))),
            'humidity': 65 + 15 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25) + np.random.normal(0, 8, len(dates)),
            'pressure': 1013 + np.random.normal(0, 5, len(dates)),
            'wind_speed': 4 + np.random.exponential(2, len(dates)),
            'latitude': dam_info['latitude'],
            'longitude': dam_info['longitude'],
            'dam_name': dam_name,
            'nearest_station': 'Sample Station'
        }
        
        df = pd.DataFrame(data)
        logger.info(f"{dam_name} için {len(df)} günlük örnek meteorolojik veri oluşturuldu")
        return df
    
    def get_weather_summary(self, weather_data: pd.DataFrame) -> Dict:
        """Meteorolojik veri özeti"""
        if weather_data.empty:
            return {"error": "Veri bulunamadı"}
        
        summary = {
            "total_days": len(weather_data),
            "date_range": {
                "start": weather_data['date'].min(),
                "end": weather_data['date'].max()
            },
            "temperature": {
                "avg_max": weather_data['temp_max'].mean(),
                "avg_min": weather_data['temp_min'].mean(),
                "max_recorded": weather_data['temp_max'].max(),
                "min_recorded": weather_data['temp_min'].min()
            },
            "precipitation": {
                "total": weather_data['precipitation'].sum(),
                "avg_daily": weather_data['precipitation'].mean(),
                "max_daily": weather_data['precipitation'].max(),
                "rainy_days": (weather_data['precipitation'] > 0).sum()
            },
            "humidity": {
                "avg": weather_data['humidity'].mean(),
                "min": weather_data['humidity'].min(),
                "max": weather_data['humidity'].max()
            },
            "pressure": {
                "avg": weather_data['pressure'].mean(),
                "min": weather_data['pressure'].min(),
                "max": weather_data['pressure'].max()
            }
        }
        
        return summary
    
    def calculate_evaporation_estimate(self, weather_data: pd.DataFrame) -> pd.Series:
        """Buharlaşma tahmini hesapla"""
        if weather_data.empty:
            return pd.Series()
        
        # Penman-Monteith benzeri basit formül
        temp_avg = (weather_data['temp_max'] + weather_data['temp_min']) / 2
        humidity = weather_data['humidity']
        wind_speed = weather_data['wind_speed']
        
        # Basit buharlaşma formülü (mm/gün)
        evaporation = (temp_avg - 10) * (1 - humidity / 100) * (1 + wind_speed / 10) * 0.1
        evaporation = np.clip(evaporation, 0, 10)  # 0-10 mm/gün arasında sınırla
        
        return evaporation
    
    def get_station_info(self) -> List[Dict]:
        """Meteoroloji istasyonu bilgileri"""
        stations_info = []
        for station in self.weather_stations.values():
            stations_info.append({
                "station_id": station.station_id,
                "name": station.name,
                "latitude": station.latitude,
                "longitude": station.longitude,
                "data_points": len(station.data)
            })
        return stations_info

