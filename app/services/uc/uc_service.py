from typing import Any, Dict, List

from .scrapper.requests import (
    request_parameters,
    request_buscacursos,
    request_requirements,
    request_vacancies
)
from app.services.base_service import BaseService
from app.models.uc import UCParameter, UCCourse, UCCourseRequirements
from .scrapper.constants import TRANSLATOR
from app.services.multithread import MultithreadJob


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
        course_info['requirements'] = request_requirements(
            course_info['course_code']
        )
        course_info['semester'] = params['semester']
        for section in course_info['sections']:
            section['semester'] = params['semester']

        job = MultithreadJob([
            [request_vacancies, [params['semester'], s['section_id']]]
            for s in course_info['sections']
        ])
        job.start()
        job.join()
        vacancies = job.get_results()

        for i in range(len(course_info['sections'])):
            section = course_info['sections'][i]
            section['vacancies'] = vacancies[i]

        return UCCourse(**course_info)

    def course_requirements(self, course_code: str):
        requirements_json = request_requirements(course_code)

        return UCCourseRequirements(**requirements_json)

    def multiple_courses(
        self,
        semester: str,
        course_codes: List[str]
    ) -> List[UCCourse]:
        jobs_args = []
        for course_code in course_codes:
            params = {"semester": semester, "course_code": course_code}
            jobs_args.append([self.course_details, [params]])
        job = MultithreadJob(jobs_args)
        job.start()
        job.join()
        courses = job.get_results()

        return list(filter(lambda c: c is not None, courses))
