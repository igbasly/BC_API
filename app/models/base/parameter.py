from typing import List, Optional
from .base_model import BaseModel


class BaseSelectValue(BaseModel):
    name: str
    value: str


class BaseParameter(BaseModel):
    name: str
    type: str
    values: Optional[List[BaseSelectValue]]


class SearchQuery(BaseModel):
    semester: Optional[str]
    campus: Optional[str]
    course_code: Optional[str]
    name: Optional[str]
    section_id: Optional[int]
