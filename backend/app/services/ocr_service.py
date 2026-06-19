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
            scale = min(target / long_edge, 3.0)
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

        try:
            osd = pytesseract.image_to_osd(image)
            match = re.search(r"Rotate: (\d+)", osd)
            if match:
                angle = int(match.group(1))
                if angle:
                    image = image.rotate(-angle, expand=True)
        except Exception:
            pass

        proc = OCRService._preprocess(image)

        extracted_text = pytesseract.image_to_string(proc, lang="tur+eng").strip()

        data = pytesseract.image_to_data(
            proc, lang="tur+eng", output_type=pytesseract.Output.DICT
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