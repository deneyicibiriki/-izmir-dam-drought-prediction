"""
Google Colab için Düzeltilmiş Komutlar
Bu dosya repository adındaki tire karakteri sorununu çözer.
"""

def get_colab_commands():
    """Colab için düzeltilmiş komutları döndür"""
    
    print("🚀 GOOGLE COLAB İÇİN DÜZELTİLMİŞ KOMUTLAR")
    print("=" * 50)
    
    print("\n📥 1. PROJE İNDİRME (DÜZELTİLMİŞ)")
    print("-" * 40)
    print("!git clone https://github.com/deneyicibiriki/-izmir-dam-drought-prediction.git")
    print("!cd '/content/-izmir-dam-drought-prediction'")
    print("# veya")
    print("!cd /content/\\-izmir-dam-drought-prediction")
    
    print("\n📦 2. KÜTÜPHANELERİ YÜKLEME")
    print("-" * 30)
    print("!pip install -r '/content/-izmir-dam-drought-prediction/requirements.txt'")
    print("!pip install beautifulsoup4 lxml pydantic-settings")
    
    print("\n🔧 3. ÇALIŞMA DİZİNİNİ AYARLA")
    print("-" * 35)
    print("import os")
    print("os.chdir('/content/-izmir-dam-drought-prediction')")
    print("print('Mevcut dizin:', os.getcwd())")
    
    print("\n🧪 4. ML ANALİZİNİ ÇALIŞTIR")
    print("-" * 30)
    print("exec(open('/content/-izmir-dam-drought-prediction/ml_methods_analysis.py').read())")
    
    print("\n🌐 5. API TESTLERİNİ ÇALIŞTIR")
    print("-" * 30)
    print("exec(open('/content/-izmir-dam-drought-prediction/colab_demo.py').read())")
    
    print("\n🚀 6. ANA UYGULAMAYI ÇALIŞTIR")
    print("-" * 30)
    print("exec(open('/content/-izmir-dam-drought-prediction/colab_setup.py').read())")
    
    print("\n💡 ALTERNATİF ÇÖZÜMLER:")
    print("-" * 25)
    print("1. Repository'yi yeniden adlandırın (tire olmadan)")
    print("2. Tam path kullanın: '/content/-izmir-dam-drought-prediction'")
    print("3. Escape karakteri kullanın: '\\-izmir-dam-drought-prediction'")
    print("4. os.chdir() fonksiyonunu kullanın")

def create_colab_notebook_code():
    """Colab notebook için hazır kod blokları"""
    
    print("\n📓 COLAB NOTEBOOK İÇİN HAZIR KOD BLOKLARI")
    print("=" * 50)
    
    print("\n🔧 HÜCRE 1: Proje İndirme")
    print("-" * 30)
    print("""
# Projeyi indir
!git clone https://github.com/deneyicibiriki/-izmir-dam-drought-prediction.git

# Çalışma dizinini ayarla
import os
os.chdir('/content/-izmir-dam-drought-prediction')
print('Mevcut dizin:', os.getcwd())

# Dosyaları listele
!ls -la
""")
    
    print("\n🔧 HÜCRE 2: Kütüphaneleri Yükleme")
    print("-" * 35)
    print("""
# Gerekli kütüphaneleri yükle
!pip install -r requirements.txt
!pip install beautifulsoup4 lxml pydantic-settings

print('✅ Tüm kütüphaneler yüklendi!')
""")
    
    print("\n🔧 HÜCRE 3: ML Analizi")
    print("-" * 25)
    print("""
# ML metodları analizini çalıştır
exec(open('ml_methods_analysis.py').read())
""")
    
    print("\n🔧 HÜCRE 4: API Testleri")
    print("-" * 25)
    print("""
# API testlerini çalıştır
exec(open('colab_demo.py').read())
""")
    
    print("\n🔧 HÜCRE 5: Ana Uygulama")
    print("-" * 25)
    print("""
# Ana uygulamayı çalıştır
from colab_setup import run_colab_app
app, report = run_colab_app()
""")

def show_alternative_solutions():
    """Alternatif çözümleri göster"""
    
    print("\n🛠️ ALTERNATİF ÇÖZÜMLER")
    print("=" * 30)
    
    print("\n1️⃣ Repository'yi Yeniden Adlandırma:")
    print("-" * 35)
    print("!git clone https://github.com/deneyicibiriki/-izmir-dam-drought-prediction.git")
    print("!mv -izmir-dam-drought-prediction izmir-dam-drought-prediction")
    print("!cd izmir-dam-drought-prediction")
    
    print("\n2️⃣ Tam Path Kullanma:")
    print("-" * 25)
    print("!cd '/content/-izmir-dam-drought-prediction'")
    print("# veya")
    print("!cd /content/\\-izmir-dam-drought-prediction")
    
    print("\n3️⃣ Python ile Dizin Değiştirme:")
    print("-" * 35)
    print("import os")
    print("os.chdir('/content/-izmir-dam-drought-prediction')")
    print("print('Mevcut dizin:', os.getcwd())")
    
    print("\n4️⃣ Symbolic Link Oluşturma:")
    print("-" * 30)
    print("!ln -s -izmir-dam-drought-prediction izmir-dam-drought-prediction")
    print("!cd izmir-dam-drought-prediction")

def main():
    """Ana fonksiyon"""
    get_colab_commands()
    create_colab_notebook_code()
    show_alternative_solutions()
    
    print("\n🎉 ÖZET")
    print("=" * 15)
    print("Repository adındaki tire karakteri sorunu için:")
    print("1. Tam path kullanın: '/content/-izmir-dam-drought-prediction'")
    print("2. os.chdir() fonksiyonunu kullanın")
    print("3. Escape karakteri kullanın: '\\-izmir-dam-drought-prediction'")
    print("4. Repository'yi yeniden adlandırın")

if __name__ == "__main__":
    main()
