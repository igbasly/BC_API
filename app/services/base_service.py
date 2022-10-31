from abc import ABC, abstractmethod


class BaseService(ABC):
    @abstractmethod
    def _translate_params(self, original_params):
        pass  # pragma: no cover

    @abstractmethod
    def authorized_params(self):
        pass  # pragma: no cover

    @abstractmethod
    def search_courses(self, params):
        pass  # pragma: no cover

    @abstractmethod
    def course_details(self, params):
        pass  # pragma: no cover

    @abstractmethod
    def course_requirements(self, course_code):
        pass  # pragma: no cover
