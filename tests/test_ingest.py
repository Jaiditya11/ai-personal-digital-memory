from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ingest():
    payload = {"text": "Learn AWS S3 basics", "source": "notion", "tags": ["AWS", "learning"]}
    response = client.post("/ingest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "stored"
    assert "id" in data 
