import io

import pytest
from PIL import Image

from backend.app.services.ocr_service import OCRService


def _make_test_image_bytes():
    image = Image.new("RGB", (60, 30), color="white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_ocr_logic_returns_expected_keys():
    result = OCRService.process_image(_make_test_image_bytes())
    assert "extracted_text" in result
    assert "confidence_score" in result
    assert "processed_at" in result
    assert isinstance(result["extracted_text"], str)


def test_file_validation_valid():
    assert OCRService.validate_file("resim.jpg") is True
    assert OCRService.validate_file("not.png") is True


def test_file_validation_invalid():
    assert OCRService.validate_file("virüs.exe") is False
    assert OCRService.validate_file("odev.pdf") is False