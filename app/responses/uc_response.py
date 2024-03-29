from typing import List, Optional, Any

from app.models.base import BaseModel
from app.models.uc import UCParameter, UCCourse


class UCResourceResponse(BaseModel):
    url: str
    resource: Optional[Any]


class UCResourcesResponse(BaseModel):
    url: str
    resources: Optional[List[Any]]


class UCParamsResponse(UCResourcesResponse):
    resources: List[UCParameter]


class UCCoursesResponse(UCResourcesResponse):
    resources: List[UCCourse]


class UCCourseResponse(UCResourceResponse):
    resource: Optional[UCCourse]
    error: Optional[str]
