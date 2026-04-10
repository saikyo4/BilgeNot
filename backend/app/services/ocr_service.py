import time

class OCRService:
    @staticmethod
    def process_image(image_bytes: bytes):
        """
        Görselden metin ayıklama işlemini simüle eder.
        Gerçek implementasyonda buraya Tesseract veya Cloud Vision gelir.
        """
        
        time.sleep(1.5) 
        
       
        return {
            "extracted_text": "BilgeNot Uygulaması - Test Notu: FastAPI ve Firebase entegrasyonu başarılı.",
            "confidence_score": 0.94,
            "processed_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def validate_file(filename: str):
        # Dosya uzantısı kontrolü
        allowed_extensions = ["png", "jpg", "jpeg"]
        ext = filename.split(".")[-1].lower()
        return ext in allowed_extensions