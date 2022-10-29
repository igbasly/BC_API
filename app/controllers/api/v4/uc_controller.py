from fastapi import APIRouter, Request, Depends
from app.models.uc.uc_parameter import UCSearchQuery
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


@router.get('/{semester}/search', response_model=UCResourcesResponse)
def get_search_courses(
    request: Request,
    params: UCSearchQuery = Depends()
):
    service = UCService()
    dict_params = params.sanitized_params()
    courses = service.search_courses(dict_params)

    return {"url": request.url._url, "resources": courses}
