from typing import List, Optional
from pydantic import BaseModel


class BaseSelectValue(BaseModel):
    name: str
    value: str


class BaseParameter(BaseModel):
    name: str
    type: str
    values: Optional[List[BaseSelectValue]]
