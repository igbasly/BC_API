from fastapi import FastAPI

from .config import MainRouter


app = FastAPI()
app.include_router(MainRouter)
