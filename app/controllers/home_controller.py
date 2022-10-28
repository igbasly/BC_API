from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter(tags=["Home"])


@router.get("/", status_code=303)
def index():
    return RedirectResponse("/redoc")
