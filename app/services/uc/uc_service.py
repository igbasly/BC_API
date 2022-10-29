from typing import Dict, Union

from app.services.uc.uc_scrappers import (
    request_parameters,
    request_buscacursos
)
from app.services.base_service import BaseService
from app.models.uc import UCParameter, UCCourse
from .constants import TRANSLATOR


class UCService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def authorized_params(self):
        params = request_parameters()

        return list(map(lambda p: UCParameter(**p), params))

    def search_courses(self, params: Dict[str, Union[str, int]]):
        bc_params = {}
        print(params)
        for key in params:
            bc_params[TRANSLATOR[key]] = params[key]

        courses_json = request_buscacursos(bc_params)
        courses = []
        for course in courses_json:
            course['semester'] = params['semester']
            for section in course['sections']:
                section['semester'] = params['semester']
            courses.append(UCCourse(**course))

        return courses
