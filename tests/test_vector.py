from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ingest_and_query():
    payload = {"text": "Learn AWS S3 basics", "source": "notion", "tags": ["AWS"]}
    response = client.post("/ingest", json=payload)
    assert response.status_code == 200

    q = client.get("/query?q=AWS")
    data = q.json()
    assert data["query"] == "AWS"
    assert any("AWS" in res[0] for res in data["results"])
