import json
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_index():
    response = client.get('/api/v4/uc/')
    base_url = client.base_url
    uc_routes = list(map(
        lambda x: {
            "url": base_url + x.path,
            "name": x.name,
            "methods": list(x.methods)},
        filter(lambda x: "/uc/" in x.path, app.routes)))

    assert response.status_code == 200
    assert response.json() == {
        "name": "UC",
        "resources": uc_routes,
        "url": response.url
    }


def test_get_params():
    response = client.get('/api/v4/uc/parameters')
    with open("./app/assets/files/uc_params.json") as file_:
        params = json.load(file_)

    data = response.json()

    assert response.status_code == 200
    assert 'resources' in data
    assert 'types' in data

    resources = data['resources']
    for key in params:
        item = list(filter(lambda x: x['name'] == key, resources))[0]
        assert item['type'] == params[key][0]
        if params[key][0] == "select":
            assert len(item['values']) > 0
        else:
            assert item['values'] is None
