from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_favicon():
    with open('app/assets/images/favicon.png', 'rb') as expected_file:
        expected_data = expected_file.read()

    response = client.get('/favicon.ico')

    assert response.status_code == 200
    assert response.content == expected_data
