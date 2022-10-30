from __future__ import annotations
from typing import List, Literal
from .base_model import BaseModel


class CourseRequirement(BaseModel):
    type = "req"
    course_code: str


class CourseRequirementRelation(BaseModel):
    type = "rel"
    relation: Literal["OR", "AND"]
    course_codes: List[CourseRequirementRelation | CourseRequirement]


class CourseRequirements(BaseModel):
    requirements: List[CourseRequirementRelation | CourseRequirement]
    restrictions: List[CourseRequirementRelation | CourseRequirement]


class ClassModule(BaseModel):
    type: str
    day: int
    module: int


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
    modules: List[ClassModule]


class Course(BaseModel):
    semester: str
    name: str
    course_code: str
    sections: List[Section]
