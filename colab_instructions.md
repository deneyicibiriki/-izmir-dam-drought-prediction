# Google Colab'da İzmir Baraj Doluluk ve Kuraklık Riski Tahmini Çalıştırma

## 🚀 Hızlı Başlangıç

### 1. Google Colab'a Erişim
1. [Google Colab](https://colab.research.google.com/) adresine gidin
2. Google hesabınızla giriş yapın
3. "New Notebook" butonuna tıklayın

### 2. Notebook'u Yükleme
**Seçenek A: GitHub'dan Yükleme (Önerilen)**
1. Colab'da "File" > "Open notebook" seçin
2. "GitHub" sekmesine tıklayın
3. Repository URL'ini girin: `https://github.com/your-username/izmir-dam-prediction`
4. `colab_notebook.ipynb` dosyasını seçin

**Seçenek B: Manuel Yükleme**
1. Bu repository'den `colab_notebook.ipynb` dosyasını indirin
2. Colab'da "File" > "Upload notebook" seçin
3. İndirdiğiniz dosyayı yükleyin

### 3. Çalıştırma
1. Notebook'taki tüm hücreleri sırayla çalıştırın (Shift+Enter)
2. İlk hücre kütüphaneleri yükleyecek (2-3 dakika sürebilir)
3. Sonraki hücreler veri oluşturacak ve analiz yapacak

## 📋 Adım Adım Kullanım

### Adım 1: Kütüphane Kurulumu
```python
# Bu hücre tüm gerekli kütüphaneleri yükler
!pip install pandas numpy matplotlib seaborn plotly scikit-learn requests
```

### Adım 2: Veri Oluşturma
- 5 İzmir barajı için 90 günlük örnek veri oluşturulur
- Baraj doluluk oranları, hava durumu verileri dahil

### Adım 3: Analiz
- Mevcut durum analizi
- Kuraklık seviyesi belirleme
- Trend analizi

### Adım 4: Tahminler
- 30 günlük gelecek tahminleri
- Kuraklık riski değerlendirmesi

### Adım 5: Görselleştirme
- İnteraktif grafikler
- Zaman serisi analizi
- Karşılaştırmalı grafikler

## 🔧 Özelleştirme

### Veri Kaynağını Değiştirme
Gerçek veri kullanmak için:

```python
# CSV dosyasından veri yükleme
import pandas as pd
dam_data = pd.read_csv('your_dam_data.csv')
weather_data = pd.read_csv('your_weather_data.csv')
```

### API Entegrasyonu
Gerçek API'lerden veri çekmek için:

```python
# API anahtarlarınızı ekleyin
OPENWEATHER_API_KEY = "your_api_key_here"
IZSU_API_KEY = "your_izsu_api_key_here"
```

### Model Parametrelerini Değiştirme
```python
# Tahmin gün sayısını değiştirin
prediction_days = 60  # 60 günlük tahmin

# Kuraklık eşiklerini ayarlayın
drought_threshold = 0.25  # %25 altı kuraklık
critical_threshold = 0.05  # %5 altı kritik
```

## 📊 Çıktılar

### 1. Analiz Sonuçları
- Baraj doluluk oranları
- Kuraklık seviyeleri
- Trend analizleri
- Genel durum özeti

### 2. Tahminler
- 30 günlük doluluk tahminleri
- Kuraklık riski skorları
- Değişim oranları

### 3. Görselleştirmeler
- İnteraktif bar grafikleri
- Zaman serisi grafikleri
- Karşılaştırmalı grafikler
- Pasta grafikleri

### 4. Uyarılar ve Öneriler
- Kritik seviye uyarıları
- Trend uyarıları
- Önlem önerileri

## 🚨 Sorun Giderme

### Yaygın Hatalar

**1. Kütüphane Yükleme Hatası**
```python
# Çözüm: Kütüphaneleri tek tek yükleyin
!pip install pandas
!pip install numpy
!pip install matplotlib
```

**2. Veri Boyutu Hatası**
```python
# Çözüm: Veri boyutunu küçültün
dam_data = dam_data.head(1000)  # İlk 1000 kayıt
```

**3. Bellek Hatası**
```python
# Çözüm: Colab'da GPU kullanın
# Runtime > Change runtime type > GPU
```

**4. Görselleştirme Hatası**
```python
# Çözüm: Plotly'i yeniden yükleyin
!pip install --upgrade plotly
```

### Performans Optimizasyonu

**1. GPU Kullanımı**
- Runtime > Change runtime type > GPU
- Daha hızlı hesaplama için

**2. Veri Önbellekleme**
```python
# Verileri önbelleğe alın
import pickle
with open('cached_data.pkl', 'wb') as f:
    pickle.dump(combined_data, f)
```

**3. Paralel İşleme**
```python
# Çoklu işlemci kullanımı
from multiprocessing import Pool
```

## 📱 Mobil Erişim

Colab mobil uygulaması ile:
1. Google Colab uygulamasını indirin
2. Notebook'unuzu açın
3. Mobil cihazınızdan analiz yapın

## 🔄 Güncellemeler

### Veri Güncelleme
```python
# Günlük veri güncelleme
def update_daily_data():
    # Yeni veri çekme kodu
    pass
```

### Model Güncelleme
```python
# Model parametrelerini güncelleme
def update_model_parameters():
    # Yeni parametreler
    pass
```

## 📞 Destek

### Yardım Alma
1. GitHub Issues: Repository'de issue açın
2. Email: [your-email@domain.com]
3. Dokümantasyon: README.md dosyasını inceleyin

### Katkıda Bulunma
1. Fork yapın
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Pull request gönderin

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---

**Not**: Bu uygulama eğitim ve araştırma amaçlıdır. Kritik kararlar için profesyonel hidrolojik analiz gereklidir.
