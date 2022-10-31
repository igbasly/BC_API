from fastapi import FastAPI

from .config import MainRouter, AppConfiguration, AppMiddlewares


app = FastAPI(
    **AppConfiguration
)
app.include_router(MainRouter)
for middleware in AppMiddlewares:
    app.add_middleware(**middleware)
