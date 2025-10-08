from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

@patch("app.main.generate_answer", return_value="Mocked answer for test")
def test_query_with_llm(mock_llm):
    payload = {"text": "Learn AWS basics", "source": "manual"}
    client.post("/ingest", json=payload)

    response = client.get("/query?q=AWS")
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] == "Mocked answer for test"
