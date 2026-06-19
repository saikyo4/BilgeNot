from fastapi import FastAPI, File, UploadFile
from datetime import datetime
from app.database import firebase_config
from app.services.ocr_service import OCRService
from pydantic import BaseModel
from app.services.gemini_service import gemini_service

ocr_service = OCRService()

app = FastAPI(
    title="BilgeNot API Service",
    description="Core backend services for BilgeNot AI Assistant",
    version="1.0.0"
)

START_TIME = datetime.now().isoformat()

@app.get("/", tags=["System"])
def health_check():
    db_connected = firebase_config.check_db_connection()
    return {
        "status": "healthy" if db_connected else "degraded",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": {"connected": db_connected},
            "ocr_engine": "ready"
        }
    }

@app.get("/api/v1/info", tags=["System"])
def get_info():
    return {
        "developer": "Egehan ALACAM",
        "institution": "Computer Engineering Department",
        "module": "Graduation Project - Phase II"
    }

@app.post("/api/v1/scan", tags=["OCR Services"])
async def scan_note(filename: str):
    if not OCRService.validate_file(filename):
        return {"status": "error", "message": "Desteklenmeyen dosya formatı!"}
    
    result = OCRService.process_image(b"fake_data")
    return {"data": result}

class AIRequest(BaseModel):
    text: str

@app.post("/api/summarize")
async def create_summary(request: AIRequest):
    result = gemini_service.summarize_text(request.text)
    return {"data": result}

@app.post("/api/quiz")
async def create_quiz(request: AIRequest):
    result = gemini_service.generate_quiz(request.text)
    return {"data": result}
    
@app.post("/api/ocr")
async def process_image_ocr(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        # GECICI TESHIS: sunucuya ulasan ham fotografi diske kaydet
        with open("/tmp/last_upload.png", "wb") as f:
            f.write(image_bytes)
        text = OCRService.process_image(image_bytes)
        return {"text": text}
    except Exception as e:
        return {"text": f"Hata: Fotoğraf okunamadı. Detay: {str(e)}"}


from fastapi.responses import FileResponse
import os


@app.get("/api/debug/last-image")
async def get_last_image():
    path = "/tmp/last_upload.png"
    if os.path.exists(path):
        return FileResponse(path, media_type="image/png")
    return {"status": "henüz bir fotoğraf yüklenmedi"}