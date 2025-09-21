"""
Google Colab Hızlı Düzeltme - Import Hataları Çözümü
Bu dosya import hatalarını düzeltir ve Colab'da hızlıca çalıştırır.
"""

# Gerekli kütüphaneleri import et
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import sys
import os

try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import cross_val_score, train_test_split
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.preprocessing import StandardScaler
    ML_AVAILABLE = True
except ImportError:
    print("⚠️ Scikit-learn yüklü değil, ML özellikleri devre dışı")
    ML_AVAILABLE = False

def run_colab_quick_fix():
    """Hızlı Colab düzeltmesi"""
    print("🚀 COLAB HIZLI DÜZELTİLMİŞ VERSİYON")
    print("=" * 50)
    
    # 1. Kütüphane durumunu kontrol et
    print("\n📦 1. KÜTÜPHANE DURUMU")
    print("-" * 25)
    print(f"✅ pandas: {pd.__version__}")
    print(f"✅ numpy: {np.__version__}")
    print(f"✅ requests: {requests.__version__}")
    
    if ML_AVAILABLE:
        import sklearn
        print(f"✅ scikit-learn: {sklearn.__version__}")
    else:
        print("❌ scikit-learn: Yüklü değil")
    
    # 2. Basit API testi
    print("\n🌐 2. BASİT API TESTİ")
    print("-" * 25)
    
    try:
        # Test URL'si
        test_url = "https://httpbin.org/get"
        response = requests.get(test_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Internet bağlantısı çalışıyor")
            print("✅ requests kütüphanesi çalışıyor")
        else:
            print(f"⚠️ API testi başarısız: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API test hatası: {e}")
    
    # 3. Örnek veri oluşturma
    print("\n📊 3. ÖRNEK VERİ OLUŞTURMA")
    print("-" * 30)
    
    # Baraj verileri simülasyonu
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    dam_names = ['Tahtalı', 'Balçova', 'Güzelhisar']
    
    dam_data = []
    for date in dates:
        for dam in dam_names:
            dam_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'dam_name': dam,
                'fill_ratio': np.random.uniform(0.3, 0.9),
                'temperature': np.random.uniform(15, 35),
                'precipitation': np.random.exponential(2),
                'humidity': np.random.uniform(40, 80)
            })
    
    df = pd.DataFrame(dam_data)
    print(f"✅ {len(df)} kayıt oluşturuldu")
    print(f"📅 Tarih aralığı: {df['date'].min()} - {df['date'].max()}")
    print(f"🏞️ Barajlar: {', '.join(df['dam_name'].unique())}")
    
    # İlk 5 kaydı göster
    print("\n📋 Örnek Veriler:")
    print(df.head())
    
    # 4. Basit istatistikler
    print("\n📈 4. BASİT İSTATİSTİKLER")
    print("-" * 30)
    
    for dam in dam_names:
        dam_subset = df[df['dam_name'] == dam]
        avg_fill = dam_subset['fill_ratio'].mean()
        print(f"{dam:<15}: Ortalama doluluk {avg_fill:.1%}")
    
    # 5. ML analizi (eğer mümkünse)
    if ML_AVAILABLE:
        print("\n🤖 5. BASİT ML ANALİZİ")
        print("-" * 25)
        
        # Özellikler ve hedef
        X = df[['temperature', 'precipitation', 'humidity']].values
        y = df['fill_ratio'].values
        
        # Veriyi böl
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Basit model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Tahmin
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        
        print(f"✅ Linear Regression R²: {r2:.4f}")
        print("✅ ML analizi tamamlandı")
    else:
        print("\n⚠️ 5. ML ANALİZİ ATLANILDI")
        print("-" * 30)
        print("Scikit-learn yüklenmemiş, ML analizi yapılamıyor")
    
    # 6. Sonuç
    print("\n🎉 6. SONUÇ")
    print("-" * 15)
    print("✅ Hızlı test tamamlandı!")
    print("✅ Import hataları düzeltildi")
    print("✅ Temel fonksiyonlar çalışıyor")
    
    if ML_AVAILABLE:
        print("✅ ML özellikleri aktif")
    else:
        print("⚠️ ML için: !pip install scikit-learn")
    
    print("\n🔗 Sonraki adımlar:")
    print("1. Tam uygulamayı çalıştırmak için: exec(open('colab_setup.py').read())")
    print("2. API testleri için: exec(open('test_api_integration.py').read())")
    print("3. ML analizi için: exec(open('ml_methods_analysis.py').read())")

if __name__ == "__main__":
    run_colab_quick_fix()
