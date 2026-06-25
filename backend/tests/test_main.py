from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert "status" in body
    assert "services" in body


def test_get_info():
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    body = response.json()
    assert "developer" in body
    assert "institution" in body


def test_scan_rejects_bad_extension():

    response = client.post("/api/v1/scan", params={"filename": "dosya.pdf"})
    assert response.status_code == 200
    assert response.json()["status"] == "error"


def test_ocr_requires_file():

    response = client.post("/api/ocr")
    assert response.status_code == 422


def test_summarize_requires_text():

    response = client.post("/api/summarize", json={})
    assert response.status_code == 422


def test_quiz_requires_text():
    response = client.post("/api/quiz", json={})
    assert response.status_code == 422