import resource
from fastapi import APIRouter


router = APIRouter(
    prefix="/uc",
    tags=["UC"]
)


@router.get('/')
def index():
    routes = list(map(
        lambda r: {"name": r.name, "url": r.path, "methods": r.methods},
        router.routes
    ))

    return {"name": router.tags[0], "resources": routes}
