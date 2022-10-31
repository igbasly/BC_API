import json
import datetime
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

    resources = data['resources']
    for key in params:
        item = list(filter(lambda x: x['name'] == key, resources))[0]
        assert item['type'] == params[key][0]
        if params[key][0] == "select":
            assert len(item['values']) > 0
        else:
            assert 'values' not in item


def test_get_search_courses_invalid_search():
    response = client.get('/api/v4/uc/1999-2/search?foo=bar')

    assert response.status_code == 200
    assert response.json()['resources'] == []


def test_get_search_courses_valid_search():
    year = datetime.date.today().year
    params = {
        "course_code": "mat1610"
    }
    response = client.get(f"/api/v4/uc/{year}-1/search", params=params)
    data = response.json()

    assert response.status_code == 200
    assert len(data['resources']) == 1
    course = data['resources'][0]
    assert "name" in course and course["course_code"] == 'MAT1610'

    for section in course['sections']:
        expected_keys = [
            'course_code', 'semester', 'section_id', 'section', 'teacher_name',
            'value', 'campus'
        ]
        for key in expected_keys:
            assert section[key] is not None
        assert len(section['modules']) > 0


def test_get_course_information_invalid():
    expected_error = "Course information not found, please check semester "\
                     "and course code"
    response_bad_params = client.get('/api/v4/uc/1999-2/HOLA123')
    year = datetime.date.today().year
    response_multiple_courses = client.get(f"/api/v4/uc/{year}-1/MAT")

    assert response_bad_params.status_code == 404
    assert response_multiple_courses.status_code == 404
    assert response_bad_params.json()['error'] == expected_error
    assert response_multiple_courses.json()['error'] == expected_error
    assert 'resource' not in response_bad_params.json()
    assert 'resource' not in response_multiple_courses.json()


def test_get_course_information_valid():
    year = datetime.date.today().year
    response = client.get(f"/api/v4/uc/{year}-1/MAT1610")
    data = response.json()

    assert response.status_code == 200
    assert 'error' not in data
    assert data['resource']['course_code'] == "MAT1610"
