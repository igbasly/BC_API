from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter(tags=["Home"])


@router.get("/", include_in_schema=False)
def index():
    return RedirectResponse("https://igbasly.github.io/BC_API/")
