import pytest
from backend.app.services.ocr_service import OCRService

def test_ocr_logic_returns_text():
    
    result = OCRService.process_image(b"fake_image_data")
    assert "extracted_text" in result
    assert len(result["extracted_text"]) > 0

def test_file_validation_valid():
    
    assert OCRService.validate_file("resim.jpg") is True
    assert OCRService.validate_file("not.png") is True

def test_file_validation_invalid():
   
    assert OCRService.validate_file("virüs.exe") is False
    assert OCRService.validate_file("odev.pdf") is False