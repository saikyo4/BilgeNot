# BilgeNot — Yapay Zekâ Destekli Mobil Ders Notu Asistanı

BilgeNot, öğrencilerin ders notlarını fotoğraftan dijitale çeviren ve yapay zekâ ile özet veya çoktan seçmeli test üreten, baştan sona çalışan bir sistemdir. Kullanıcı bir ders notunun fotoğrafını çeker, sistem yazıyı metne çevirir, ardından bu metinden özet ya da test üretip sonucu veritabanına kaydeder.

## Özellikler

- Fotoğraftan metin çıkarma (Türkçe destekli)
- Metinden otomatik özet üretme
- Metinden çoktan seçmeli test üretme
- Üretilen sonuçların veritabanına kaydedilmesi
- Hem Android hem web üzerinde çalışma
- Bulutta canlı yayın

## Kullanılan Teknolojiler

- Sunucu: Python 3.12, FastAPI
- Metin tanıma: Tesseract
- Yapay zekâ: Google Gemini
- Veritabanı: Firebase Firestore
- Paketleme: Docker
- Otomatik test ve dağıtım: GitHub Actions
- Yayın: Render (sunucu), Netlify (web)

## Test

Proje birim testleriyle kontrol edilmektedir. Test kapsamı %66 düzeyindedir ve tüm testler başarıyla geçmektedir.

## Canlı Adresler

- Web uygulaması: https://tiny-paprenjak-c6ebad.netlify.app
- Sunucu: https://bilgenot.onrender.com
- API dokümantasyonu: https://bilgenot.onrender.com/docs

## Kurulum

1. Gerekli kütüphaneleri yükleyin:
   `pip install -r backend/requirements.txt`
2. Sunucuyu başlatın:
   `uvicorn backend.app.main:app --reload`