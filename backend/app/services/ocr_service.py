import io
import re
import time

import pytesseract
from PIL import Image, ImageOps


class OCRService:
    @staticmethod
    def process_image(image_bytes: bytes):
        """
        Görselden Tesseract OCR ile metin ayıklar (Türkçe + İngilizce).
        Fotoğrafın dönük (ters/yan) olma ihtimaline karşı otomatik düzeltir.
        """
        image = Image.open(io.BytesIO(image_bytes))

        # 1) Telefonun gömdüğü EXIF dönme bilgisini uygula (en sık sorun bu)
        image = ImageOps.exif_transpose(image)

        # 2) Tesseract'in kendi yön algılamasi (OSD) ile ek düzeltme dene
        try:
            osd = pytesseract.image_to_osd(image)
            match = re.search(r"Rotate: (\d+)", osd)
            if match:
                angle = int(match.group(1))
                if angle:
                    # OSD "saat yonunde su kadar donmus" der; geri cevirmek icin -angle
                    image = image.rotate(-angle, expand=True)
        except Exception:
            # OSD bazen kucuk/az yazili gorsellerde calismaz; sorun degil, devam
            pass

        # 3) Metni çıkar
        extracted_text = pytesseract.image_to_string(image, lang="tur+eng").strip()

        # 4) Ortalama güven skoru
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