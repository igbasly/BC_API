from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter(tags=["Home"])


@router.get("/", status_code=303, include_in_schema=False)
def index():
    return RedirectResponse("http://igbasly.github.io/BC_API/")
