from ..main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_summary_request_valid():
    response = client.post("/summary", json={
        "doc": "hello",
        "source": "www.google.com",
        "task_type": "summary",
        "api_token": "XXXX",
    })
    assert response.status_code == 422

    response = client.post("/summary", json={
        "doc": "hello",
        "source": "www.google.com",
        "task_type": "summary",
        "api_token": "XXXX",
    })
    assert response.status_code == 422
