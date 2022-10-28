from fastapi import APIRouter


router = APIRouter(tags=["Home"])


@router.get("/")
def index():
    return {"hello": "world!"}
