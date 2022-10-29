from typing import List, Optional
from pydantic import BaseModel


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

    def sanitized_params(self):
        params = self.dict()
        new_dict = {}
        for key in params:
            if params[key] is not None:
                new_dict[key] = params[key]

        return new_dict
