from typing import List
from pydantic import BaseModel


class ClassModules(BaseModel):
    day: int
    module: int
    type: str


class Section(BaseModel):
    semester: str
    name: str
    course_code: str
    section: int
    section_id: int
    english_version: bool
    format: str
    category: str
    teacher_name: str
    campus: str
    value: int
    total_vacancies: int
    available_vacancies: int
    modules: List[ClassModules]


class Course(BaseModel):
    semester: str
    name: str
    course_code: str
    sections: List[Section]
