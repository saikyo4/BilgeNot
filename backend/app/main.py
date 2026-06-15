from fastapi import FastAPI
from datetime import datetime
from app.database import firebase_config
from backend.app.services.ocr_service import OCRService

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
    return {
        "status": "success",
        "request_file": filename,
        "data": result
    }
