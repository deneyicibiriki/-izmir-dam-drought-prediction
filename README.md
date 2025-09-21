# İzmir Baraj Doluluk ve Kuraklık Riski Tahmini

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/deneyicibiriki/-izmir-dam-drought-prediction/blob/main/colab_setup.py)

Bu proje, İzmir bölgesi barajlarının doluluk oranlarını ve kuraklık riskini tahmin etmek için geliştirilmiş OOP tabanlı bir Python uygulamasıdır.

## 🌟 Özellikler

- **Gerçek API Entegrasyonu**: İZSU ve Open-Meteo API'leri
- **5 İzmir Barajı**: Tahtalı, Balçova, Güzelhisar, Çamlı, Gediz
- **OOP Tabanlı Mimari**: Modüler ve genişletilebilir yapı
- **Google Colab Desteği**: Ücretsiz çalıştırma
- **Makine Öğrenmesi**: Gelecek 30 günlük tahmin
- **İnteraktif Görselleştirme**: Plotly grafikleri

## 🚀 Hızlı Başlangıç

### Google Colab'da Çalıştırma (Önerilen)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/deneyicibiriki/-izmir-dam-drought-prediction/blob/main/colab_setup.py)

1. Yukarıdaki "Open In Colab" butonuna tıklayın
2. Tüm hücreleri sırayla çalıştırın
3. Sonuçları görüntüleyin

### Yerel Kurulum
```bash
# Repository'yi klonlayın
git clone https://github.com/deneyicibiriki/-izmir-dam-drought-prediction.git
cd -izmir-dam-drought-prediction

# Sanal ortam oluşturun
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Uygulamayı çalıştırın
python main.py
```

## 📊 API Entegrasyonları

### İZSU (İzmir Su ve Kanalizasyon İdaresi)
- **URL**: https://www.izsu.gov.tr/tr/baraj-doluluk-oranlari
- **Veri**: Baraj doluluk oranları, su seviyeleri
- **Güncelleme**: Günlük

### Open-Meteo (Hava Durumu)
- **URL**: https://api.open-meteo.com/v1
- **Veri**: Sıcaklık, yağış, nem, basınç, rüzgar
- **Güncelleme**: Gerçek zamanlı
- **API Anahtarı**: Gerekmez (ücretsiz)

## 🏗️ Proje Yapısı

```
izmir_dam_prediction/
├── config/              # Konfigürasyon dosyaları
├── data/                # Veri dosyaları
├── models/              # OOP modelleri
├── services/            # API servisleri
├── utils/               # Yardımcı fonksiyonlar
├── tests/               # Test dosyaları
├── main.py              # Ana uygulama
├── colab_setup.py       # Colab için optimize edilmiş kod
└── requirements.txt     # Python bağımlılıkları
```

## 📈 Kullanım Örnekleri

### Temel Kullanım
```python
from main import IzmirDamPredictionApp

# Uygulamayı başlat
app = IzmirDamPredictionApp()

# Veri kaynaklarını ayarla
app.setup_data_sources(dam_source="api", weather_source="api")

# Verileri yükle
app.load_dam_data()
app.load_weather_data()

# Analiz yap
analysis = app.analyze_dams()
predictions = app.predict_future_levels(30)

# Rapor oluştur
report = app.generate_report()
```

### Google Colab Kullanımı
```python
# Colab'da çalıştır
from colab_setup import run_colab_app
app, report = run_colab_app()
```

## 🧪 Test

```bash
# API entegrasyonlarını test et
python test_api_integration.py

# Ana uygulamayı test et
python main.py
```

## 🔧 Geliştirme

### Katkıda Bulunma
1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

- **GitHub Issues**: [Issues](https://github.com/deneyicibiriki/-izmir-dam-drought-prediction/issues)
- **Repository**: https://github.com/deneyicibiriki/-izmir-dam-drought-prediction

## 🙏 Teşekkürler

- [İZSU](https://www.izsu.gov.tr/) - İzmir Su ve Kanalizasyon İdaresi
- [Open-Meteo](https://open-meteo.com/) - Açık kaynak meteoroloji API'si
- [scikit-learn](https://scikit-learn.org/) - Makine öğrenmesi kütüphanesi

---

**Not**: Bu uygulama eğitim ve araştırma amaçlıdır. Kritik kararlar için profesyonel hidrolojik analiz gereklidir.