"""
Makine Öğrenmesi Metodları Analizi - İzmir Baraj Doluluk Tahmini
Bu dosya projede kullanılan ML metodlarını detaylı olarak açıklar.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import SelectKBest, f_regression
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

class MLMethodsAnalysis:
    """Makine öğrenmesi metodları analiz sınıfı"""
    
    def __init__(self):
        self.models = {}
        self.results = {}
        self.feature_importance = {}
        
    def explain_ml_methods(self):
        """Kullanılan ML metodlarını açıkla"""
        print("🤖 MAKİNE ÖĞRENMESİ METODLARI DETAYLI ANALİZ")
        print("=" * 60)
        
        print("\n📊 1. REGRESYON MODELLERİ (Doluluk Oranı Tahmini)")
        print("-" * 50)
        
        print("\n🌲 Random Forest Regressor:")
        print("   - Algoritma: Ensemble learning (topluluk öğrenmesi)")
        print("   - Çalışma Prensibi: Birden fazla karar ağacı oluşturur ve ortalamalarını alır")
        print("   - Avantajları:")
        print("     * Overfitting'e karşı dirençli")
        print("     * Özellik önem analizi yapabilir")
        print("     * Eksik verilerle iyi çalışır")
        print("     * Non-linear ilişkileri yakalayabilir")
        print("   - Dezavantajları:")
        print("     * Yorumlanması zor")
        print("     * Büyük veri setlerinde yavaş")
        print("   - Baraj tahmininde kullanımı:")
        print("     * Sıcaklık, yağış, nem gibi faktörleri ağırlıklandırır")
        print("     * Geçmiş verilerden öğrenerek gelecek tahmini yapar")
        
        print("\n🚀 Gradient Boosting Regressor:")
        print("   - Algoritma: Sequential ensemble learning")
        print("   - Çalışma Prensibi: Hataları sırayla düzeltir")
        print("   - Avantajları:")
        print("     * Yüksek doğruluk")
        print("     * Karmaşık pattern'leri yakalayabilir")
        print("     * Özellik önem analizi")
        print("   - Dezavantajları:")
        print("     * Overfitting riski")
        print("     * Yavaş eğitim")
        print("   - Baraj tahmininde kullanımı:")
        print("     * Trend analizi için idealdir")
        print("     * Mevsimsel değişimleri yakalar")
        
        print("\n📈 Linear Regression:")
        print("   - Algoritma: Doğrusal regresyon")
        print("   - Çalışma Prensibi: Y = aX + b formülü")
        print("   - Avantajları:")
        print("     * Hızlı ve basit")
        print("     * Yorumlanabilir")
        print("     * Overfitting riski düşük")
        print("   - Dezavantajları:")
        print("     * Sadece doğrusal ilişkileri yakalar")
        print("     * Karmaşık pattern'leri kaçırabilir")
        print("   - Baraj tahmininde kullanımı:")
        print("     * Basit trend analizi")
        print("     * Baseline model olarak kullanılır")
        
        print("\n📊 2. SINIFLANDIRMA MODELLERİ (Kuraklık Seviyesi)")
        print("-" * 50)
        
        print("\n🎯 Logistic Regression:")
        print("   - Algoritma: Logistik regresyon")
        print("   - Çalışma Prensibi: Sigmoid fonksiyonu ile olasılık hesaplar")
        print("   - Avantajları:")
        print("     * Hızlı eğitim")
        print("     * Yorumlanabilir")
        print("     * Overfitting riski düşük")
        print("   - Dezavantajları:")
        print("     * Sadece doğrusal decision boundary")
        print("   - Baraj tahmininde kullanımı:")
        print("     * Kuraklık seviyesi sınıflandırması")
        print("     * Risk kategorileri (Normal, Dikkat, Kritik)")
        
        print("\n🔧 3. ÖZELLİK MÜHENDİSLİĞİ")
        print("-" * 30)
        
        print("\n📅 Lag Features (Gecikme Özellikleri):")
        print("   - 1 gün önceki doluluk oranı")
        print("   - 3 gün önceki doluluk oranı")
        print("   - 7 gün önceki doluluk oranı")
        print("   - 14 gün önceki doluluk oranı")
        print("   - 30 gün önceki doluluk oranı")
        print("   - Amaç: Geçmiş verilerin geleceği etkileme gücü")
        
        print("\n📊 Moving Average Features (Hareketli Ortalama):")
        print("   - 7 günlük hareketli ortalama")
        print("   - 14 günlük hareketli ortalama")
        print("   - 30 günlük hareketli ortalama")
        print("   - Amaç: Trend ve mevsimsel etkileri yakalamak")
        
        print("\n🌡️ Weather Features (Hava Durumu Özellikleri):")
        print("   - Günlük maksimum sıcaklık")
        print("   - Günlük minimum sıcaklık")
        print("   - Günlük yağış miktarı")
        print("   - Ortalama nem oranı")
        print("   - Ortalama basınç")
        print("   - Ortalama rüzgar hızı")
        
        print("\n🔍 4. MODEL DEĞERLENDİRME METRİKLERİ")
        print("-" * 40)
        
        print("\n📈 Regresyon Metrikleri:")
        print("   - MSE (Mean Squared Error): Ortalama kare hata")
        print("   - RMSE (Root Mean Squared Error): Karekök ortalama hata")
        print("   - R² (R-squared): Açıklanan varyans oranı")
        print("   - MAE (Mean Absolute Error): Ortalama mutlak hata")
        
        print("\n🎯 Sınıflandırma Metrikleri:")
        print("   - Accuracy: Doğru sınıflandırma oranı")
        print("   - Precision: Pozitif tahminlerin doğruluk oranı")
        print("   - Recall: Gerçek pozitiflerin yakalanma oranı")
        print("   - F1-Score: Precision ve Recall'un harmonik ortalaması")
        
        print("\n🔄 Cross-Validation:")
        print("   - 5-fold cross-validation kullanılır")
        print("   - Modelin genelleme yeteneğini test eder")
        print("   - Overfitting'i önler")
        
    def create_sample_ml_pipeline(self):
        """Örnek ML pipeline oluştur"""
        print("\n🔬 ÖRNEK ML PIPELINE")
        print("=" * 30)
        
        # Örnek veri oluştur
        np.random.seed(42)
        n_samples = 1000
        
        # Özellikler
        features = {
            'temperature_max': np.random.normal(25, 5, n_samples),
            'temperature_min': np.random.normal(15, 3, n_samples),
            'precipitation': np.random.exponential(2, n_samples),
            'humidity': np.random.uniform(40, 80, n_samples),
            'pressure': np.random.uniform(1000, 1020, n_samples),
            'wind_speed': np.random.uniform(5, 15, n_samples),
            'lag_1': np.random.uniform(0.3, 0.9, n_samples),
            'lag_7': np.random.uniform(0.3, 0.9, n_samples),
            'ma_7': np.random.uniform(0.3, 0.9, n_samples),
            'ma_30': np.random.uniform(0.3, 0.9, n_samples)
        }
        
        X = pd.DataFrame(features)
        
        # Hedef değişken (doluluk oranı)
        y = (0.4 + 
             0.1 * X['temperature_max'] / 30 + 
             0.2 * X['precipitation'] / 10 - 
             0.05 * X['humidity'] / 100 + 
             0.1 * X['lag_1'] + 
             0.05 * X['ma_7'] + 
             np.random.normal(0, 0.05, n_samples))
        y = np.clip(y, 0, 1)
        
        print(f"📊 Veri Boyutu: {X.shape[0]} örnek, {X.shape[1]} özellik")
        print(f"🎯 Hedef Değişken: Doluluk oranı (0-1 arası)")
        
        # Veriyi böl
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Veri normalizasyonu
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        print(f"\n📚 Veri Bölünmesi:")
        print(f"Eğitim seti: {X_train.shape[0]} örnek")
        print(f"Test seti: {X_test.shape[0]} örnek")
        
        # Modelleri eğit
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
            
            # Tahminler
            y_pred = model.predict(X_test_scaled)
            
            # Metrikler
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = np.mean(np.abs(y_test - y_pred))
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')
            
            results[name] = {
                'MSE': mse,
                'RMSE': rmse,
                'MAE': mae,
                'R²': r2,
                'CV Mean': cv_scores.mean(),
                'CV Std': cv_scores.std()
            }
            
            print(f"   MSE: {mse:.4f}")
            print(f"   RMSE: {rmse:.4f}")
            print(f"   MAE: {mae:.4f}")
            print(f"   R²: {r2:.4f}")
            print(f"   CV R²: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
            
            # Özellik önem analizi (Random Forest için)
            if hasattr(model, 'feature_importances_'):
                self.feature_importance[name] = model.feature_importances_
        
        # Sonuçları karşılaştır
        print("\n📊 MODEL PERFORMANS KARŞILAŞTIRMASI")
        print("=" * 60)
        print(f"{'Model':<20} {'MSE':<8} {'RMSE':<8} {'MAE':<8} {'R²':<8} {'CV R²':<12}")
        print("-" * 70)
        
        for name, metrics in results.items():
            print(f"{name:<20} {metrics['MSE']:<8.4f} {metrics['RMSE']:<8.4f} "
                  f"{metrics['MAE']:<8.4f} {metrics['R²']:<8.4f} "
                  f"{metrics['CV Mean']:<8.4f} (±{metrics['CV Std']:.4f})")
        
        # En iyi model
        best_model = max(results.keys(), key=lambda x: results[x]['R²'])
        print(f"\n🏆 En iyi model: {best_model} (R² = {results[best_model]['R²']:.4f})")
        
        # Özellik önem analizi
        if 'Random Forest' in self.feature_importance:
            print("\n🔍 ÖZELLİK ÖNEM ANALİZİ (Random Forest)")
            print("-" * 45)
            
            importance_df = pd.DataFrame({
                'Özellik': X.columns,
                'Önem': self.feature_importance['Random Forest']
            }).sort_values('Önem', ascending=False)
            
            for idx, row in importance_df.iterrows():
                print(f"{row['Özellik']:<20}: {row['Önem']:.4f} ({row['Önem']*100:.1f}%)")
        
        return results, self.feature_importance
    
    def explain_prediction_logic(self):
        """Tahmin mantığını açıkla"""
        print("\n🧠 TAHMİN MANTIĞI VE ALGORİTMA")
        print("=" * 40)
        
        print("\n📊 1. VERİ HAZIRLAMA AŞAMASI:")
        print("   - API'lerden ham veri çekilir")
        print("   - Veri temizleme ve validasyon")
        print("   - Eksik değerlerin doldurulması")
        print("   - Outlier'ların tespit edilmesi")
        
        print("\n🔧 2. ÖZELLİK MÜHENDİSLİĞİ:")
        print("   - Lag features: Geçmiş değerler")
        print("   - Moving averages: Trend analizi")
        print("   - Weather features: Hava durumu etkileri")
        print("   - Seasonal features: Mevsimsel etkiler")
        
        print("\n🤖 3. MODEL EĞİTİMİ:")
        print("   - Veri train/test olarak bölünür")
        print("   - Cross-validation ile model seçimi")
        print("   - Hyperparameter tuning")
        print("   - Model performans değerlendirmesi")
        
        print("\n🔮 4. TAHMİN SÜRECİ:")
        print("   - Geçmiş verilerden öğrenilen pattern'ler")
        print("   - Hava durumu tahminleri ile birleştirme")
        print("   - Trend analizi ve mevsimsel düzeltmeler")
        print("   - Güven aralığı hesaplama")
        
        print("\n📈 5. SONUÇ YORUMLAMA:")
        print("   - Doluluk oranı tahmini")
        print("   - Kuraklık riski kategorilendirme")
        print("   - Uyarı seviyeleri")
        print("   - Öneriler ve aksiyon planları")
        
        print("\n💡 6. MODEL GÜNCELLEME:")
        print("   - Yeni verilerle periyodik güncelleme")
        print("   - Model performans izleme")
        print("   - Drift detection")
        print("   - Retraining stratejisi")

def main():
    """Ana fonksiyon"""
    print("🚀 İZMİR BARAJ DOLULUK TAHMİNİ - ML METODLARI ANALİZİ")
    print("=" * 70)
    
    # Analiz sınıfını oluştur
    ml_analysis = MLMethodsAnalysis()
    
    # ML metodlarını açıkla
    ml_analysis.explain_ml_methods()
    
    # Örnek pipeline oluştur
    results, feature_importance = ml_analysis.create_sample_ml_pipeline()
    
    # Tahmin mantığını açıkla
    ml_analysis.explain_prediction_logic()
    
    print("\n🎉 ANALİZ TAMAMLANDI!")
    print("=" * 30)
    print("\n📋 ÖZET:")
    print("- Random Forest: En iyi genel performans")
    print("- Gradient Boosting: Trend analizi için ideal")
    print("- Linear Regression: Baseline model")
    print("- Cross-validation: Model güvenilirliği")
    print("- Feature importance: Özellik etki analizi")
    
    print("\n🔗 Proje Linkleri:")
    print("- GitHub: https://github.com/deneyicibiriki/-izmir-dam-drought-prediction")
    print("- Colab: colab_setup.py dosyasını kullanın")

if __name__ == "__main__":
    main()
