from fastapi import APIRouter, Request
from app.responses import UCResourcesResponse

from app.services import UCService


router = APIRouter(
    prefix="/uc",
    tags=["UC"]
)


@router.get('/', response_model=UCResourcesResponse)
def index(request: Request):
    base_url = request.url._url
    routes = list(map(
        lambda r: {
            "name": r.name,
            "url": f"{base_url}{r.path.replace('/uc/', '')}",
            "methods": r.methods,
        },
        router.routes
    ))

    return {"name": router.tags[0], "resources": routes, "url": base_url}


@router.get('/parameters', response_model=UCResourcesResponse)
def get_parameters(request: Request):
    service = UCService()
    params = service.authorized_params()

    return {"resources": params, "url": request.url._url}
