import io
import time

import pytesseract
from PIL import Image, ImageOps


class OCRService:
    @staticmethod
    def _preprocess(image: Image.Image) -> Image.Image:
        proc = image.convert("L")

        # Cok buyuk gorselleri kucult (hiz icin) - Tesseract az pikselde hizli calisir
        max_edge = 1800
        long_edge = max(proc.size)
        if long_edge > max_edge:
            scale = max_edge / long_edge
            proc = proc.resize(
                (int(proc.width * scale), int(proc.height * scale)),
                Image.Resampling.LANCZOS,
            )

        proc = ImageOps.autocontrast(proc, cutoff=2)
        return proc

    @staticmethod
    def process_image(image_bytes: bytes):
        image = Image.open(io.BytesIO(image_bytes))
        image = ImageOps.exif_transpose(image)

        proc = OCRService._preprocess(image)

        # Tek gecisde hem metin hem guven skoru
        data = pytesseract.image_to_data(
            proc, lang="tur", output_type=pytesseract.Output.DICT
        )

        kelimeler = []
        confidences = []
        for i, kelime in enumerate(data.get("text", [])):
            kelime = kelime.strip()
            if not kelime:
                continue
            kelimeler.append(kelime)
            try:
                c = float(data["conf"][i])
                if c >= 0:
                    confidences.append(c)
            except (TypeError, ValueError, IndexError):
                pass

        extracted_text = " ".join(kelimeler)
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