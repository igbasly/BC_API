from fastapi import APIRouter, Request
from app.models import base

from app.services import UCService


router = APIRouter(
    prefix="/uc",
    tags=["UC"]
)


@router.get('/')
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


@router.get('/parameters')
def get_parameters():
    service = UCService()
    params = service.authorized_params()
    types = list(set(map(lambda x: x.type, params)))

    return {"resources": params, "types": types}
