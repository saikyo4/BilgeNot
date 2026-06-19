import io

from PIL import Image

from app.services.ocr_service import OCRService
from app.services import gemini_service as gs
from app.services import db_service as dbs


def _blank_image_bytes():
    image = Image.new("RGB", (80, 40), color="white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


# --- OCR servisi testleri ---

def test_ocr_returns_all_keys():
    result = OCRService.process_image(_blank_image_bytes())
    assert set(result.keys()) == {"extracted_text", "confidence_score", "processed_at"}


def test_ocr_confidence_is_number():
    result = OCRService.process_image(_blank_image_bytes())
    assert isinstance(result["confidence_score"], float)
    assert 0.0 <= result["confidence_score"] <= 1.0


def test_validate_file_accepts_images():
    assert OCRService.validate_file("a.png") is True
    assert OCRService.validate_file("b.JPG") is True
    assert OCRService.validate_file("c.jpeg") is True


def test_validate_file_rejects_others():
    assert OCRService.validate_file("x.pdf") is False
    assert OCRService.validate_file("y.exe") is False
    assert OCRService.validate_file("z.txt") is False


# --- LLM (Gemini) servisi testleri ---

def test_summarize_empty_text():
    service = gs.GeminiService()
    assert service.summarize_text("") == "Özetlenecek metin bulunamadı."


def test_quiz_empty_text():
    service = gs.GeminiService()
    assert service.generate_quiz("") == "Quiz oluşturulacak metin bulunamadı."


# --- Veritabani servisi testi ---

def test_db_save_handles_no_connection(monkeypatch):
    monkeypatch.setattr(dbs.firebase_config, "db", None)
    result = dbs.DBService.save_result("summarize", "girdi", "cikti")
    assert result is None