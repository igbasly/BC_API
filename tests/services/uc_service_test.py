from app.models.uc import UCParameter
from app.models.uc import UCCourseRequirements
from app.services import UCService, BaseService


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


def test_method_course_requirements():
    test = UCService()
    response = test.course_requirements("IIC2233")

    assert type(response) is UCCourseRequirements
    assert len(response.requirements) == 1
    assert len(response.equivalencies) == 1
