import pytest
from app.services import BaseService


class ServiceMock(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def authorized_params(self):
        return {}

    def search_courses(self, params):
        return []

    def _translate_params(self, original_params):
        return original_params

    def course_details(self, params):
        return {}

    def course_requirements(self, course_code):
        return {}

    def section_vancancies(self, semester, section_id):
        return {}


def test_base_service_class():
    # Check if it's a Abstract class
    with pytest.raises(TypeError):
        BaseService()


def test_abstract_methods_not_defined():
    with pytest.raises(TypeError):
        class TestService(BaseService):
            def __init__(self) -> None:
                super().__init__()

        # raise TypeRrror because of abstract methods
        TestService()


def test_abstract_methods_defined():
    test = ServiceMock()

    assert test.authorized_params() == {}
    assert test.search_courses("") == []
    assert test._translate_params("") == ""
    assert test.course_details("") == {}
