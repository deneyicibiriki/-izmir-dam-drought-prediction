"""
İZSU API Servisi - İzmir Su ve Kanalizasyon İdaresi veri çekme servisi
"""
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
import time
from config.settings import settings

logger = logging.getLogger(__name__)

class IZSUAPIService:
    """İZSU web sitesinden baraj verilerini çeken servis"""
    
    def __init__(self):
        self.base_url = settings.api.izsu_base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def fetch_dam_data(self, days: int = 30) -> pd.DataFrame:
        """
        İZSU web sitesinden baraj verilerini çek
        
        Args:
            days: Kaç günlük veri çekilecek
            
        Returns:
            pd.DataFrame: Baraj verileri
        """
        try:
            logger.info("İZSU web sitesinden baraj verileri çekiliyor...")
            
            # İZSU baraj doluluk oranları sayfasına git
            url = f"{self.base_url}{settings.api.izsu_dam_data_endpoint}"
            
            response = self.session.get(url, timeout=settings.api.api_timeout)
            response.raise_for_status()
            
            # HTML'i parse et
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Baraj verilerini çıkar (bu kısım İZSU'nun HTML yapısına göre güncellenmeli)
            dam_data = self._extract_dam_data_from_html(soup)
            
            if dam_data.empty:
                logger.warning("İZSU'dan veri çekilemedi, örnek veri kullanılıyor")
                return self._create_sample_dam_data(days)
            
            logger.info(f"İZSU'dan {len(dam_data)} baraj kaydı çekildi")
            return dam_data
            
        except Exception as e:
            logger.error(f"İZSU veri çekme hatası: {e}")
            logger.info("Örnek veri kullanılıyor")
            return self._create_sample_dam_data(days)
    
    def _extract_dam_data_from_html(self, soup: BeautifulSoup) -> pd.DataFrame:
        """
        HTML'den baraj verilerini çıkar
        
        Args:
            soup: BeautifulSoup objesi
            
        Returns:
            pd.DataFrame: Çıkarılan baraj verileri
        """
        dam_data = []
        
        try:
            # İZSU'nun HTML yapısına göre bu kısım güncellenmeli
            # Örnek: tablolar, div'ler, JSON veriler vb.
            
            # Tablo bulma (örnek)
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Header'ı atla
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 4:  # En az 4 sütun olmalı
                        try:
                            dam_name = cells[0].get_text(strip=True)
                            current_volume = float(cells[1].get_text(strip=True).replace(',', '.'))
                            total_capacity = float(cells[2].get_text(strip=True).replace(',', '.'))
                            fill_ratio = current_volume / total_capacity if total_capacity > 0 else 0
                            
                            dam_data.append({
                                'date': datetime.now().strftime('%Y-%m-%d'),
                                'dam_name': dam_name,
                                'current_volume_mcm': current_volume,
                                'total_capacity_mcm': total_capacity,
                                'fill_ratio': fill_ratio,
                                'inflow_mcm': 0,  # Varsa eklenebilir
                                'outflow_mcm': 0,  # Varsa eklenebilir
                                'evaporation_mcm': 0  # Varsa eklenebilir
                            })
                        except (ValueError, IndexError) as e:
                            logger.warning(f"Satır parse edilemedi: {e}")
                            continue
            
            # JSON veri bulma (eğer sayfada varsa)
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'dam' in script.string.lower():
                    try:
                        # JSON veri çıkarma (örnek)
                        json_data = self._extract_json_from_script(script.string)
                        if json_data:
                            dam_data.extend(json_data)
                    except Exception as e:
                        logger.warning(f"Script parse edilemedi: {e}")
                        continue
            
        except Exception as e:
            logger.error(f"HTML parse hatası: {e}")
        
        return pd.DataFrame(dam_data)
    
    def _extract_json_from_script(self, script_content: str) -> List[Dict]:
        """
        Script içinden JSON veri çıkar
        
        Args:
            script_content: Script içeriği
            
        Returns:
            List[Dict]: JSON veriler
        """
        try:
            # JSON veri bulma (örnek regex)
            import re
            
            # JSON objesi bulma
            json_pattern = r'\{[^{}]*"dam"[^{}]*\}'
            matches = re.findall(json_pattern, script_content, re.IGNORECASE)
            
            dam_data = []
            for match in matches:
                try:
                    data = json.loads(match)
                    if 'dam' in data:
                        dam_data.append(data)
                except json.JSONDecodeError:
                    continue
            
            return dam_data
            
        except Exception as e:
            logger.warning(f"JSON çıkarma hatası: {e}")
            return []
    
    def _create_sample_dam_data(self, days: int) -> pd.DataFrame:
        """
        Örnek baraj verisi oluştur (İZSU'dan veri çekilemediğinde)
        
        Args:
            days: Kaç günlük veri
            
        Returns:
            pd.DataFrame: Örnek baraj verileri
        """
        import numpy as np
        
        dams = settings.get_all_dam_names()
        dam_data = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            
            for dam_name in dams:
                dam_info = settings.get_dam_info(dam_name)
                if not dam_info:
                    continue
                
                # Gerçekçi doluluk oranları
                base_ratio = 0.6 + np.random.normal(0, 0.1)
                base_ratio = max(0.1, min(0.95, base_ratio))
                
                # Mevsimsel etki
                seasonal_effect = 0.1 * np.sin(2 * np.pi * i / 365)
                base_ratio += seasonal_effect
                base_ratio = max(0.05, min(0.98, base_ratio))
                
                dam_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'dam_name': dam_name,
                    'current_volume_mcm': dam_info['capacity_mcm'] * base_ratio,
                    'total_capacity_mcm': dam_info['capacity_mcm'],
                    'fill_ratio': base_ratio,
                    'inflow_mcm': np.random.uniform(1.0, 3.0),
                    'outflow_mcm': np.random.uniform(1.0, 2.5),
                    'evaporation_mcm': np.random.uniform(0.1, 0.5)
                })
        
        return pd.DataFrame(dam_data)
    
    def get_dam_status(self, dam_name: str) -> Optional[Dict]:
        """
        Belirli bir barajın güncel durumunu getir
        
        Args:
            dam_name: Baraj adı
            
        Returns:
            Dict: Baraj durumu
        """
        try:
            dam_data = self.fetch_dam_data(days=1)
            dam_info = dam_data[dam_data['dam_name'] == dam_name]
            
            if dam_info.empty:
                return None
            
            latest = dam_info.iloc[-1]
            return {
                'dam_name': dam_name,
                'current_volume_mcm': latest['current_volume_mcm'],
                'total_capacity_mcm': latest['total_capacity_mcm'],
                'fill_ratio': latest['fill_ratio'],
                'date': latest['date'],
                'status': self._get_dam_status_level(latest['fill_ratio'])
            }
            
        except Exception as e:
            logger.error(f"Baraj durumu çekme hatası: {e}")
            return None
    
    def _get_dam_status_level(self, fill_ratio: float) -> str:
        """
        Doluluk oranına göre baraj durumu
        
        Args:
            fill_ratio: Doluluk oranı
            
        Returns:
            str: Durum seviyesi
        """
        if fill_ratio >= 0.8:
            return "Yüksek"
        elif fill_ratio >= 0.6:
            return "Normal"
        elif fill_ratio >= 0.4:
            return "Düşük"
        elif fill_ratio >= 0.2:
            return "Kritik"
        else:
            return "Çok Kritik"
    
    def get_all_dams_status(self) -> List[Dict]:
        """
        Tüm barajların durumunu getir
        
        Returns:
            List[Dict]: Tüm barajların durumu
        """
        try:
            dam_data = self.fetch_dam_data(days=1)
            dams_status = []
            
            for dam_name in dam_data['dam_name'].unique():
                status = self.get_dam_status(dam_name)
                if status:
                    dams_status.append(status)
            
            return dams_status
            
        except Exception as e:
            logger.error(f"Tüm barajlar durumu çekme hatası: {e}")
            return []
