# BilgeNot - Yapay Zeka Destekli Ders Notu Asistanı

Bu proje, öğrencilerin ders notlarını OCR teknolojisi ile dijitalleştiren ve yapay zeka ile özetleyen bir sistemdir.

## 🚀 Mevcut Özellikler (Vize Aşaması)
- **Backend:** FastAPI mimarisi üzerine kurulu, katmanlı yapı (Layered Architecture).
- **Database:** Firebase Firestore entegrasyonu tamamlandı.
- **OCR Service:** Simüle edilmiş OCR motoru ve dosya doğrulama sistemi.
- **CI/CD:** GitHub Actions ile otomatik test süreçleri (Pipeline) aktif.

## 🛠️ Teknik Detaylar
- **Dil:** Python 3.12
- **Framework:** FastAPI
- **Test:** Pytest (%20+ coverage)
- **Konteynerleştirme:** Dockerfile hazır.

## 📋 Kurulum
1. `pip install -r backend/requirements.txt`
2. `uvicorn backend.app.main:app --reload`
