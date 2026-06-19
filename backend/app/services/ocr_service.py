import io
import re
import time

import pytesseract
from PIL import Image, ImageOps, ImageFilter


class OCRService:
    @staticmethod
    def _preprocess(image: Image.Image) -> Image.Image:
        proc = image.convert("L")

        long_edge = max(proc.size)
        target = 1600
        if long_edge < target:
            scale = min(target / long_edge, 2.5)
            proc = proc.resize(
                (int(proc.width * scale), int(proc.height * scale)),
                Image.Resampling.LANCZOS,
            )
        elif long_edge > 2500:
            scale = 2500 / long_edge
            proc = proc.resize(
                (int(proc.width * scale), int(proc.height * scale)),
                Image.Resampling.LANCZOS,
            )

        proc = ImageOps.autocontrast(proc, cutoff=2)
        proc = proc.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=3))

        return proc

    @staticmethod
    def process_image(image_bytes: bytes):
        image = Image.open(io.BytesIO(image_bytes))
        image = ImageOps.exif_transpose(image)

        proc = OCRService._preprocess(image)

        data = pytesseract.image_to_data(
            proc, lang="tur+eng", output_type=pytesseract.Output.DICT
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