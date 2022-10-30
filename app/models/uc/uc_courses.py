from typing import List, Literal, Optional, Dict
from app.models.base import (
    Section,
    Course,
    ClassModule,
    CourseRequirements,
    CourseRequirement,
    CourseRequirementRelation,
    BaseModel
)


class UCSchool(BaseModel):
    code: str
    name: str


class UCVacancy(BaseModel):
    type: Literal['school', 'free', 'program']
    school: Optional[UCSchool]
    program: Optional[str]
    major: Optional[str]
    total: int
    available: int
    unavailable: int


class UCSectionVacancies(BaseModel):
    total: int
    available: int
    vacancies: List[UCVacancy]


class UCSection(Section):
    allow_withdrawal: bool
    need_special_approval: bool
    general_education: Optional[str]
    category: Optional[str]
    modules: List[ClassModule]
    vacancies: Optional[UCSectionVacancies]


class UCCourseRequirements(CourseRequirements):
    equivalencies: List[CourseRequirementRelation | CourseRequirement]


class UCCourse(Course):
    sections: List[UCSection]
    requirements: Optional[UCCourseRequirements]
