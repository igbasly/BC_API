import pytest
from copy import deepcopy
from pydantic import ValidationError
from app.models.base import ClassModule, Section, Course


fake_course = {
    "semester": "Foo",
    "name": "Bar",
    "course_code": "HOLA123",
    "sections": []
}

fake_section = {
    "semester": "Foo",
    "name": "Hola",
    "course_code": "HOLA213",
    "section": 1,
    "section_id": 45678,
    "english_version": False,
    "format": "Boo",
    "category": "",
    "teacher_name": "John Doe",
    "campus": "Chile",
    "value": 0,
    "total_vacancies": 2,
    "available_vacancies": 1,
    "modules": []
}

fake_module = {
    "day": 1,
    "module": 2,
    "type": "Foo"
}


def test_course_model_with_no_attributes():
    with pytest.raises(ValidationError):
        Course(**{})


def test_course_model_with_attributes():
    data = deepcopy(fake_course)
    for i in range(3):
        sec = deepcopy(fake_section)
        sec['section'] = i
        data['sections'].append(sec)

    course = Course(**data)
    assert course.course_code == fake_course['course_code']
    assert len(course.sections) == 3
    assert list(course.get_attributes().keys()) == list(data.keys())


def test_section_model_with_no_attributes():
    with pytest.raises(ValidationError):
        Section(**{})


def test_section_model_attributes():
    data = deepcopy(fake_section)
    for i in range(3):
        sec = deepcopy(fake_module)
        sec['day'] = i
        data['modules'].append(sec)

    section = Section(**data)
    assert section.section_id == fake_section['section_id']
    assert len(section.modules) == 3
    assert list(section.get_attributes().keys()) == list(data.keys())


def test_module_model_with_no_attributes():
    with pytest.raises(ValidationError):
        ClassModule(**{})


def test_module_model_attributes():
    data = deepcopy(fake_module)

    module = ClassModule(**data)
    assert module.type == fake_module['type']
    assert list(module.get_attributes().keys()) == list(data.keys())
