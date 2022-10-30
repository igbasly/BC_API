from typing import Any, Dict

from .scrapper.requests import (
    request_parameters,
    request_buscacursos
)
from app.services.base_service import BaseService
from app.models.uc import UCParameter, UCCourse
from .scrapper.constants import TRANSLATOR


class UCService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def _translate_params(self, original_params: Dict[str, Any]):
        bc_params = {}
        for key in original_params:
            bc_params[TRANSLATOR[key]] = original_params[key]

        return bc_params

    def authorized_params(self):
        params = request_parameters()

        return list(map(lambda p: UCParameter(**p), params))

    def search_courses(self, params: Dict[str, Any]):
        new_params = self._translate_params(params)
        courses_json = request_buscacursos(new_params)
        courses = []
        for course in courses_json:
            course['semester'] = params['semester']
            for section in course['sections']:
                section['semester'] = params['semester']
            courses.append(UCCourse(**course))

        return courses

    def course_details(self, params: Dict[str, str]):
        new_params = self._translate_params(params)
        courses_json = request_buscacursos(new_params)
        if len(courses_json) != 1:
            return

        course_info = courses_json[0]
        course_info['semester'] = params['semester']
        for section in course_info['sections']:
            section['semester'] = params['semester']

        return UCCourse(**course_info)
