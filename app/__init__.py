from fastapi import FastAPI

from .config import MainRouter, AppConfiguration


app = FastAPI(
    **AppConfiguration
)
app.include_router(MainRouter)
