"""
API Entegrasyon Test Dosyası
Gerçek API'lerin çalışıp çalışmadığını test eder
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.izsu_api_service import IZSUAPIService
from services.weather_api_service import WeatherAPIService
import pandas as pd
from datetime import datetime

def test_izsu_api():
    """İZSU API'sini test et"""
    print("🧪 İZSU API Testi Başlatılıyor...")
    print("=" * 50)
    
    try:
        izsu_service = IZSUAPIService()
        
        # Test veri çekme
        print("📊 Baraj verileri çekiliyor...")
        dam_data = izsu_service.fetch_dam_data(days=7)
        
        if not dam_data.empty:
            print(f"✅ {len(dam_data)} baraj kaydı çekildi")
            print(f"📅 Veri aralığı: {dam_data['date'].min()} - {dam_data['date'].max()}")
            print(f"🏞️ Barajlar: {', '.join(dam_data['dam_name'].unique())}")
            
            # İlk 3 kaydı göster
            print("\n📋 Örnek Veriler:")
            print(dam_data.head(3))
            
            # Baraj durumu testi
            print("\n🔍 Baraj Durumu Testi:")
            for dam_name in dam_data['dam_name'].unique()[:2]:  # İlk 2 baraj
                status = izsu_service.get_dam_status(dam_name)
                if status:
                    print(f"  {dam_name}: {status['fill_ratio']:.1%} - {status['status']}")
            
            return True
        else:
            print("❌ Veri çekilemedi")
            return False
            
    except Exception as e:
        print(f"❌ İZSU API Test Hatası: {e}")
        return False

def test_weather_api():
    """Hava durumu API'sini test et"""
    print("\n🧪 Hava Durumu API Testi Başlatılıyor...")
    print("=" * 50)
    
    try:
        weather_service = WeatherAPIService()
        
        # Test veri çekme
        print("🌤️ Hava durumu verileri çekiliyor...")
        dam_names = ["Tahtalı", "Balçova"]
        weather_data = weather_service.fetch_weather_data(dam_names, days=7)
        
        if not weather_data.empty:
            print(f"✅ {len(weather_data)} hava durumu kaydı çekildi")
            print(f"📅 Veri aralığı: {weather_data['date'].min()} - {weather_data['date'].max()}")
            print(f"🌡️ Sıcaklık aralığı: {weather_data['temp_max'].min():.1f}°C - {weather_data['temp_max'].max():.1f}°C")
            print(f"🌧️ Yağış toplamı: {weather_data['precipitation'].sum():.1f} mm")
            
            # İlk 3 kaydı göster
            print("\n📋 Örnek Veriler:")
            print(weather_data.head(3))
            
            # Güncel hava durumu testi
            print("\n🔍 Güncel Hava Durumu Testi:")
            current_weather = weather_service.get_current_weather("Tahtalı")
            if current_weather:
                print(f"  Tahtalı: {current_weather['temperature']:.1f}°C, "
                      f"{current_weather['precipitation']:.1f}mm yağış")
            
            return True
        else:
            print("❌ Hava durumu verisi çekilemedi")
            return False
            
    except Exception as e:
        print(f"❌ Hava Durumu API Test Hatası: {e}")
        return False

def test_colab_setup():
    """Colab setup'ı test et"""
    print("\n🧪 Colab Setup Testi Başlatılıyor...")
    print("=" * 50)
    
    try:
        # Colab setup'ı import et
        from colab_setup import IZSUAPIService as ColabIZSU, WeatherAPIService as ColabWeather
        
        print("📊 Colab İZSU servisi test ediliyor...")
        colab_izsu = ColabIZSU()
        dam_data = colab_izsu.fetch_dam_data(days=3)
        
        if not dam_data.empty:
            print(f"✅ Colab İZSU: {len(dam_data)} kayıt")
        else:
            print("❌ Colab İZSU: Veri çekilemedi")
        
        print("🌤️ Colab Weather servisi test ediliyor...")
        colab_weather = ColabWeather()
        weather_data = colab_weather.fetch_weather_data(["Tahtalı"], days=3)
        
        if not weather_data.empty:
            print(f"✅ Colab Weather: {len(weather_data)} kayıt")
        else:
            print("❌ Colab Weather: Veri çekilemedi")
        
        return True
        
    except Exception as e:
        print(f"❌ Colab Setup Test Hatası: {e}")
        return False

def test_data_integration():
    """Veri entegrasyonunu test et"""
    print("\n🧪 Veri Entegrasyon Testi Başlatılıyor...")
    print("=" * 50)
    
    try:
        from colab_setup import SimpleIzmirDamApp
        
        print("🚀 Uygulama başlatılıyor...")
        app = SimpleIzmirDamApp()
        
        print("📊 Veriler yükleniyor...")
        app.load_data()
        
        if app.dam_data is not None and app.weather_data is not None:
            print(f"✅ Baraj verisi: {len(app.dam_data)} kayıt")
            print(f"✅ Hava durumu verisi: {len(app.weather_data)} kayıt")
            
            print("🔄 Veriler işleniyor...")
            app.process_data()
            
            if not app.combined_data.empty:
                print(f"✅ Birleştirilmiş veri: {len(app.combined_data)} kayıt")
                
                print("📈 Analiz yapılıyor...")
                app.analysis = app.analyze_dams()
                
                if app.analysis:
                    print(f"✅ {len(app.analysis)} baraj analiz edildi")
                    
                    # İlk barajın analizini göster
                    first_dam = list(app.analysis.keys())[0]
                    analysis = app.analysis[first_dam]
                    print(f"  {first_dam}: {analysis['current_fill_ratio']:.1%} - {analysis['drought_level']}")
                
                return True
            else:
                print("❌ Veri birleştirme başarısız")
                return False
        else:
            print("❌ Veri yükleme başarısız")
            return False
            
    except Exception as e:
        print(f"❌ Veri Entegrasyon Test Hatası: {e}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🚀 API Entegrasyon Testleri Başlatılıyor...")
    print("=" * 60)
    print(f"📅 Test Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: İZSU API
    izsu_result = test_izsu_api()
    test_results.append(("İZSU API", izsu_result))
    
    # Test 2: Weather API
    weather_result = test_weather_api()
    test_results.append(("Weather API", weather_result))
    
    # Test 3: Colab Setup
    colab_result = test_colab_setup()
    test_results.append(("Colab Setup", colab_result))
    
    # Test 4: Data Integration
    integration_result = test_data_integration()
    test_results.append(("Data Integration", integration_result))
    
    # Sonuçları göster
    print("\n📊 TEST SONUÇLARI")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ BAŞARILI" if result else "❌ BAŞARISIZ"
        print(f"{test_name:20} : {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"Toplam: {passed}/{total} test başarılı")
    
    if passed == total:
        print("🎉 Tüm testler başarılı! Proje GitHub'a yüklenmeye hazır.")
    else:
        print("⚠️ Bazı testler başarısız. Lütfen hataları kontrol edin.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
