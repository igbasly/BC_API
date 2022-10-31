from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_index():
    response = client.get('/')

    assert response.url == "https://igbasly.github.io/BC_API/"
