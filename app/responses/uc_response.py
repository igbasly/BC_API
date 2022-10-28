from typing import List, Optional, Any
from pydantic import BaseModel


class UCResourceResponse(BaseModel):
    url: str
    resource: Optional[Any]


class UCResourcesResponse(BaseModel):
    url: str
    resources: Optional[List[Any]]
