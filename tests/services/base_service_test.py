import pytest
from app.services import BaseService


class ServiceMock(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def authorized_params(self):
        return {}

    def search_courses(self, params):
        return []


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
