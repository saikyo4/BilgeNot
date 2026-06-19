import io
import time

import pytesseract
from PIL import Image


class OCRService:
    @staticmethod
    def process_image(image_bytes: bytes):
        """
        Görselden Tesseract OCR ile metin ayıklar (Türkçe + İngilizce).
        """
        image = Image.open(io.BytesIO(image_bytes))

        extracted_text = pytesseract.image_to_string(image, lang="tur+eng").strip()

        data = pytesseract.image_to_data(
            image, lang="tur+eng", output_type=pytesseract.Output.DICT
        )
        confidences = []
        for c in data.get("conf", []):
            try:
                value = float(c)
            except (TypeError, ValueError):
                continue
            if value >= 0:
                confidences.append(value)
        confidence_score = (
            round(sum(confidences) / len(confidences) / 100, 2) if confidences else 0.0
        )

        return {
            "extracted_text": extracted_text,
            "confidence_score": confidence_score,
            "processed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @staticmethod
    def validate_file(filename: str):
        allowed_extensions = ["png", "jpg", "jpeg"]
        ext = filename.split(".")[-1].lower()
        return ext in allowed_extensions