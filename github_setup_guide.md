# GitHub Repository Oluşturma ve Yükleme Rehberi

## 🚀 GitHub Repository Oluşturma

### 1. GitHub Hesabı Oluşturma
1. [GitHub.com](https://github.com) adresine gidin
2. "Sign up" butonuna tıklayın
3. Kullanıcı adı, email ve şifre girin
4. Email doğrulaması yapın

### 2. Yeni Repository Oluşturma
1. GitHub'da giriş yaptıktan sonra sağ üst köşedeki "+" butonuna tıklayın
2. "New repository" seçin
3. Repository bilgilerini doldurun:
   - **Repository name**: `izmir-dam-drought-prediction`
   - **Description**: `İzmir Baraj Doluluk ve Kuraklık Riski Tahmini - OOP Tabanlı Python Uygulaması`
   - **Visibility**: Public (herkes görebilir) veya Private (sadece siz)
   - **Initialize**: README.md, .gitignore, license ekleyin

### 3. Repository Ayarları
- ✅ Add a README file
- ✅ Add .gitignore (Python seçin)
- ✅ Choose a license (MIT License önerilir)

## 📁 Proje Dosyalarını Hazırlama

### 1. Gerekli Dosyalar
Proje dizininizde şu dosyalar olmalı:
```
izmir_dam_prediction/
├── config/
│   └── settings.py
├── data/
│   ├── izmir_dam_data.csv
│   └── izmir_weather_data.csv
├── models/
│   └── dam.py
├── services/
│   ├── data_service.py
│   ├── weather_service.py
│   ├── izsu_api_service.py
│   └── weather_api_service.py
├── utils/
├── tests/
├── main.py
├── colab_setup.py
├── colab_instructions.md
├── requirements.txt
├── requirements_simple.txt
├── README.md
└── .gitignore
```

### 2. .gitignore Dosyası Oluşturma
Proje kök dizininde `.gitignore` dosyası oluşturun:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log

# Data files (büyük dosyalar)
data/*.csv
data/*.xlsx
data/*.json

# Results
results/
output/

# API Keys
.env
config.ini

# OS
.DS_Store
Thumbs.db
```

### 3. README.md Güncelleme
Mevcut README.md dosyasını GitHub için güncelleyin:

```markdown
# İzmir Baraj Doluluk ve Kuraklık Riski Tahmini

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/izmir-dam-drought-prediction)

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
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/izmir-dam-drought-prediction/blob/main/colab_setup.py)

1. Yukarıdaki "Open In Colab" butonuna tıklayın
2. Tüm hücreleri sırayla çalıştırın
3. Sonuçları görüntüleyin

### Yerel Kurulum
```bash
# Repository'yi klonlayın
git clone https://github.com/YOUR_USERNAME/izmir-dam-drought-prediction.git
cd izmir-dam-drought-prediction

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

## 🔧 Geliştirme

### Katkıda Bulunma
1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### Test
```bash
python -m pytest tests/
```

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

- **GitHub Issues**: [Issues](https://github.com/YOUR_USERNAME/izmir-dam-drought-prediction/issues)
- **Email**: your-email@domain.com

## 🙏 Teşekkürler

- [İZSU](https://www.izsu.gov.tr/) - İzmir Su ve Kanalizasyon İdaresi
- [Open-Meteo](https://open-meteo.com/) - Açık kaynak meteoroloji API'si
- [scikit-learn](https://scikit-learn.org/) - Makine öğrenmesi kütüphanesi

---

**Not**: Bu uygulama eğitim ve araştırma amaçlıdır. Kritik kararlar için profesyonel hidrolojik analiz gereklidir.
```

## 🔧 Git Komutları

### 1. Git Kurulumu
```bash
# Git'in yüklü olup olmadığını kontrol edin
git --version

# Eğer yüklü değilse, https://git-scm.com/ adresinden indirin
```

### 2. Git Konfigürasyonu
```bash
# Kullanıcı bilgilerini ayarlayın
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. Repository'yi Yerel Bilgisayara Klonlama
```bash
# GitHub'dan repository'yi klonlayın
git clone https://github.com/YOUR_USERNAME/izmir-dam-drought-prediction.git
cd izmir-dam-drought-prediction
```

### 4. Dosyaları Git'e Ekleme
```bash
# Tüm dosyaları ekle
git add .

# Belirli dosyaları ekle
git add main.py colab_setup.py

# Değişiklikleri commit et
git commit -m "İlk commit: İzmir baraj doluluk tahmini projesi"

# GitHub'a push et
git push origin main
```

### 5. Güncellemeler
```bash
# Değişiklikleri kontrol et
git status

# Değişiklikleri ekle
git add .

# Commit et
git commit -m "API entegrasyonları eklendi"

# Push et
git push origin main
```

## 🌐 GitHub Pages ile Web Sitesi

### 1. GitHub Pages Aktifleştirme
1. Repository'de "Settings" sekmesine gidin
2. Sol menüden "Pages" seçin
3. Source olarak "Deploy from a branch" seçin
4. Branch olarak "main" seçin
5. "Save" butonuna tıklayın

### 2. Web Sitesi URL'i
- URL: `https://YOUR_USERNAME.github.io/izmir-dam-drought-prediction`
- 5-10 dakika sonra aktif olur

## 📱 Mobil Erişim

GitHub mobil uygulaması ile:
1. GitHub mobil uygulamasını indirin
2. Repository'nizi açın
3. Kodları mobil cihazınızdan görüntüleyin

## 🔒 Güvenlik

### API Anahtarları
- API anahtarlarınızı `.env` dosyasında saklayın
- `.env` dosyasını `.gitignore`'a ekleyin
- GitHub'da "Secrets" kullanın

### Örnek .env Dosyası
```env
OPENWEATHER_API_KEY=your_api_key_here
IZSU_API_KEY=your_izsu_api_key_here
```

## 📊 İstatistikler

GitHub'da projenizin istatistiklerini görmek için:
1. Repository'de "Insights" sekmesine gidin
2. "Traffic" bölümünden ziyaretçi sayılarını görün
3. "Contributors" bölümünden katkıda bulunanları görün

## 🎯 Sonraki Adımlar

1. **Repository'yi oluşturun**
2. **Dosyaları yükleyin**
3. **README.md'yi güncelleyin**
4. **Colab badge'ini ekleyin**
5. **Issues ve Discussions'ı aktifleştirin**
6. **GitHub Pages'i kurun**
7. **Projeyi paylaşın**

---

**İpucu**: GitHub'da projenizi daha görünür yapmak için:
- Açıklayıcı README.md yazın
- Screenshot'lar ekleyin
- Demo linkleri paylaşın
- Issues ve Discussions'ı aktif tutun
- Düzenli güncellemeler yapın
