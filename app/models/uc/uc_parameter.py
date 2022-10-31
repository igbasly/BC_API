from typing import Optional, List
from fastapi import Query

from app.models.base import BaseParameter, SearchQuery, BaseModel


class UCParameter(BaseParameter):
    pass


class UCSearchQuery(SearchQuery):
    category: Optional[str]
    school: Optional[str]
    format: Optional[str]
    general_education: Optional[str]
    teacher_name: Optional[str]


class UCCourseInfoQuery(BaseModel):
    semester: str
    course_code: str


class UCMultipleCoursesQuery(BaseModel):
    semester: str
    course_codes: str
