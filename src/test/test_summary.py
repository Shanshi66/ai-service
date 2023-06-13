from ..main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_summary():
    with open('src/test/cases/chatgpt.txt', 'r') as f:
        doc = f.read()
    response = client.post("/summary", json={
        "doc": doc,
        "source": "https://www.google.com",
        "task_type": "summary",
        "api_token": "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",
    })
    print(response)
