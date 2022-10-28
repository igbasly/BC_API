from app.services import UCService, BaseService
from app.models.uc import UCParameter


def test_base_service_class():
    test = UCService()
    assert isinstance(test, UCService)
    assert isinstance(test, BaseService)


def test_method_authorized_params():
    test = UCService()
    params = test.authorized_params()

    assert type(params) == list
    for param in params:
        assert type(param) is UCParameter
