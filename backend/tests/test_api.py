from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_speech_rate_api():
    res = client.get("/speech-rate", params={"words": 150, "seconds": 60})
    assert res.json() == {"wpm": 150.0}
