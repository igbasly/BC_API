from typing import Optional
from app.models.base import BaseParameter, SearchQuery


class UCParameter(BaseParameter):
    pass


class UCSearchQuery(SearchQuery):
    category: Optional[str]
    school: Optional[str]
    format: Optional[str]
    general_education: Optional[str]
    teacher_name: Optional[str]
