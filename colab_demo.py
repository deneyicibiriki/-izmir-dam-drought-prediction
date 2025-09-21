"""
Google Colab Demo - İzmir Baraj Doluluk ve Kuraklık Riski Tahmini
Bu dosya Colab'da çalıştırılmak üzere hazırlanmıştır.
"""

def run_colab_demo():
    """Colab demo'yu çalıştır"""
    print("🚀 İZMİR BARAJ DOLULUK VE KURAKLIK RİSKİ TAHMİNİ - COLAB DEMO")
    print("=" * 70)
    print("Repository: https://github.com/deneyicibiriki/-izmir-dam-drought-prediction")
    print("=" * 70)
    
    # 1. Projeyi GitHub'dan çek
    print("\n📥 1. PROJE İNDİRME")
    print("-" * 30)
    print("!git clone https://github.com/deneyicibiriki/-izmir-dam-drought-prediction.git")
    print("!cd -izmir-dam-drought-prediction")
    
    # 2. Kütüphaneleri yükle
    print("\n📦 2. KÜTÜPHANELERİ YÜKLEME")
    print("-" * 30)
    print("!pip install -r requirements.txt")
    print("!pip install beautifulsoup4 lxml")
    
    # 3. Gerçek API testleri
    print("\n🌐 3. GERÇEK API TESTLERİ")
    print("-" * 30)
    
    try:
        # Proje modüllerini import et
        import sys
        import os
        sys.path.append('/content/-izmir-dam-drought-prediction')
        
        from services.izsu_api_service import IZSUAPIService
        from services.weather_api_service import WeatherAPIService
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta
        
        print("✅ Modüller başarıyla import edildi")
        
        # İZSU API testi
        print("\n🏞️ İZSU API Testi:")
        izsu_service = IZSUAPIService()
        dam_data = izsu_service.fetch_dam_data(days=7)
        
        if not dam_data.empty:
            print(f"✅ {len(dam_data)} baraj kaydı çekildi")
            print(f"📅 Veri aralığı: {dam_data['date'].min()} - {dam_data['date'].max()}")
            print(f"🏞️ Barajlar: {', '.join(dam_data['dam_name'].unique())}")
            
            # İlk 3 kaydı göster
            print("\n📋 Örnek Baraj Verileri:")
            print(dam_data.head(3))
        else:
            print("❌ İZSU verisi çekilemedi")
        
        # Weather API testi
        print("\n🌤️ Weather API Testi:")
        weather_service = WeatherAPIService()
        dam_names = ["Tahtalı", "Balçova", "Güzelhisar"]
        weather_data = weather_service.fetch_weather_data(dam_names, days=7)
        
        if not weather_data.empty:
            print(f"✅ {len(weather_data)} hava durumu kaydı çekildi")
            print(f"📅 Veri aralığı: {weather_data['date'].min()} - {weather_data['date'].max()}")
            print(f"🌡️ Sıcaklık aralığı: {weather_data['temp_max'].min():.1f}°C - {weather_data['temp_max'].max():.1f}°C")
            
            # İlk 3 kaydı göster
            print("\n📋 Örnek Hava Durumu Verileri:")
            print(weather_data.head(3))
        else:
            print("❌ Hava durumu verisi çekilemedi")
            
    except Exception as e:
        print(f"❌ API test hatası: {e}")
        print("🔧 Alternatif: Örnek veri kullanılacak")
    
    # 4. Makine öğrenmesi metodları
    print("\n🤖 4. MAKİNE ÖĞRENMESİ METODLARI")
    print("-" * 40)
    
    try:
        from config.settings import settings
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.linear_model import LinearRegression
        from sklearn.model_selection import cross_val_score, train_test_split
        from sklearn.metrics import mean_squared_error, r2_score
        from sklearn.preprocessing import StandardScaler
        
        print("✅ Makine öğrenmesi kütüphaneleri yüklendi")
        
        print("\n📊 Model Konfigürasyonu:")
        print(f"Tahmin Gün Sayısı: {settings.model.prediction_days}")
        print(f"Kuraklık Eşik Değeri: {settings.model.drought_threshold}")
        print(f"Kritik Seviye Eşik Değeri: {settings.model.critical_threshold}")
        print(f"Desteklenen Model Tipleri: {settings.model.model_types}")
        print(f"Cross-Validation Fold Sayısı: {settings.model.cross_validation_folds}")
        print(f"Test Set Oranı: {settings.model.test_size}")
        
        print("\n🔧 Özellik Mühendisliği:")
        print(f"Lag Özellik Günleri: {settings.model.lag_features}")
        print(f"Hareketli Ortalama Pencereleri: {settings.model.moving_average_windows}")
        
        print("\n✅ Kullanılan Makine Öğrenmesi Metodları:")
        print("- RandomForestRegressor: Ensemble yöntemi, ağaç tabanlı")
        print("- GradientBoostingRegressor: Gradient boosting, sıralı öğrenme")
        print("- LinearRegression: Doğrusal regresyon, basit ve hızlı")
        print("- Cross-validation: Model performansını değerlendirme")
        print("- StandardScaler: Veri normalizasyonu")
        
    except Exception as e:
        print(f"❌ ML kütüphane hatası: {e}")
    
    # 5. Örnek model oluşturma
    print("\n🔬 5. ÖRNEK MODEL OLUŞTURMA")
    print("-" * 35)
    
    try:
        # Örnek veri oluştur
        np.random.seed(42)
        n_samples = 100
        
        # Özellikler (features)
        X = np.random.randn(n_samples, 5)
        feature_names = ['Sıcaklık', 'Yağış', 'Nem', 'Basınç', 'Rüzgar']
        
        # Hedef değişken (target) - doluluk oranı
        y = 0.3 + 0.1 * X[:, 0] + 0.2 * X[:, 1] - 0.05 * X[:, 2] + np.random.normal(0, 0.1, n_samples)
        y = np.clip(y, 0, 1)
        
        print(f"📊 Veri Boyutu: {X.shape[0]} örnek, {X.shape[1]} özellik")
        print(f"🎯 Hedef Değişken: Doluluk oranı (0-1 arası)")
        print(f"📈 Hedef değişken istatistikleri:")
        print(f"   Ortalama: {y.mean():.3f}")
        print(f"   Standart sapma: {y.std():.3f}")
        print(f"   Min: {y.min():.3f}")
        print(f"   Max: {y.max():.3f}")
        
        # Veriyi eğitim ve test setlerine böl
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"\n📚 Veri Bölünmesi:")
        print(f"Eğitim seti: {X_train.shape[0]} örnek")
        print(f"Test seti: {X_test.shape[0]} örnek")
        
        # Veri normalizasyonu
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        print("\n🔧 Veri normalizasyonu uygulandı")
        
        # Modelleri eğit ve karşılaştır
        print("\n🤖 MODEL KARŞILAŞTIRMASI")
        print("-" * 30)
        
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }
        
        results = {}
        
        for name, model in models.items():
            print(f"\n🔧 {name} eğitiliyor...")
            
            # Modeli eğit
            model.fit(X_train_scaled, y_train)
            
            # Tahminler yap
            y_pred = model.predict(X_test_scaled)
            
            # Performans metrikleri
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Cross-validation skoru
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')
            
            results[name] = {
                'MSE': mse,
                'R²': r2,
                'CV Mean': cv_scores.mean(),
                'CV Std': cv_scores.std()
            }
            
            print(f"   MSE: {mse:.4f}")
            print(f"   R²: {r2:.4f}")
            print(f"   CV R²: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
        
        # Sonuçları karşılaştır
        print("\n📊 MODEL PERFORMANS KARŞILAŞTIRMASI")
        print("=" * 50)
        print(f"{'Model':<20} {'MSE':<10} {'R²':<10} {'CV R²':<15}")
        print("-" * 55)
        
        for name, metrics in results.items():
            print(f"{name:<20} {metrics['MSE']:<10.4f} {metrics['R²']:<10.4f} {metrics['CV Mean']:<10.4f} (±{metrics['CV Std']:.4f})")
        
        # En iyi modeli belirle
        best_model = max(results.keys(), key=lambda x: results[x]['R²'])
        print(f"\n🏆 En iyi model: {best_model} (R² = {results[best_model]['R²']:.4f})")
        
        # Özellik önem analizi
        print("\n🔍 ÖZELLİK ÖNEM ANALİZİ")
        print("-" * 30)
        
        rf_model = models['Random Forest']
        feature_importance = rf_model.feature_importances_
        
        importance_df = pd.DataFrame({
            'Özellik': feature_names,
            'Önem': feature_importance
        }).sort_values('Önem', ascending=False)
        
        print("\n📊 Özellik Önem Sıralaması:")
        for idx, row in importance_df.iterrows():
            print(f"{row['Özellik']:<15}: {row['Önem']:.4f} ({row['Önem']*100:.1f}%)")
        
    except Exception as e:
        print(f"❌ Model oluşturma hatası: {e}")
    
    # 6. Gerçek projeyi çalıştır
    print("\n🚀 6. GERÇEK PROJE ÇALIŞTIRMA")
    print("-" * 35)
    
    try:
        from colab_setup import run_colab_app
        
        print("\n📊 Uygulama başlatılıyor...")
        print("Bu işlem gerçek API'lerden veri çekecek ve analiz yapacak.")
        print("\n⏳ Lütfen bekleyin...")
        
        # Uygulamayı çalıştır
        app, report = run_colab_app()
        
        print("\n✅ Uygulama başarıyla tamamlandı!")
        
        # Rapor özetini göster
        if 'summary' in report:
            summary = report['summary']
            print(f"\n📊 ANALİZ ÖZETİ:")
            print(f"Toplam Baraj Sayısı: {summary.get('total_dams', 0)}")
            print(f"Ortalama Doluluk Oranı: {summary.get('average_fill_ratio', 0):.1%}")
            print(f"Kritik Seviyedeki Barajlar: {summary.get('critical_dams', 0)}")
            print(f"Genel Durum: {summary.get('overall_status', 'Bilinmiyor')}")
        
        # Uyarıları göster
        if 'alerts' in report and report['alerts']:
            print(f"\n🚨 UYARILAR ({len(report['alerts'])}):")
            for alert in report['alerts'][:5]:
                print(f"  - {alert.get('message', 'Uyarı')}")
        
        print("\n🎉 Analiz tamamlandı! Yukarıdaki grafikleri inceleyebilirsiniz.")
        
    except Exception as e:
        print(f"\n❌ Proje çalıştırma hatası: {e}")
        print("\n🔧 Alternatif olarak test dosyasını çalıştırabilirsiniz:")
        print("!python test_api_integration.py")
    
    # 7. Sonuç
    print("\n🎉 SONUÇ")
    print("=" * 20)
    print("\nBu demo'da gördükleriniz:")
    print("\n🤖 Makine Öğrenmesi Metodları:")
    print("1. Random Forest Regressor: Ağaç tabanlı ensemble yöntemi")
    print("2. Gradient Boosting Regressor: Sıralı öğrenme yöntemi")
    print("3. Linear Regression: Doğrusal regresyon")
    print("4. Cross-Validation: Model performans değerlendirmesi")
    print("5. Feature Importance: Özellik önem analizi")
    
    print("\n🌐 Gerçek API Entegrasyonları:")
    print("1. İZSU API: İzmir baraj verileri")
    print("2. Open-Meteo API: Hava durumu verileri")
    print("3. Fallback Mekanizması: API çalışmazsa örnek veri")
    
    print("\n📊 Analiz Yetenekleri:")
    print("1. 5 İzmir Barajı: Tahtalı, Balçova, Güzelhisar, Çamlı, Gediz")
    print("2. Kuraklık Riski: Otomatik risk değerlendirmesi")
    print("3. Tahmin Sistemi: 30 günlük gelecek tahminleri")
    print("4. Görselleştirme: İnteraktif grafikler")
    
    print("\n🔗 Proje Linkleri:")
    print("- GitHub: https://github.com/deneyicibiriki/-izmir-dam-drought-prediction")
    print("- Colab: Yukarıdaki 'Open In Colab' butonunu kullanın")
    
    print("\nProje tamamen açık kaynak ve ücretsiz olarak kullanılabilir!")

if __name__ == "__main__":
    run_colab_demo()
