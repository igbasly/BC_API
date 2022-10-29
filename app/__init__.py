from fastapi import FastAPI

from .config import MainRouter


app = FastAPI(
    title="BuscaCursos UC API",
    description="REST API para obtener información desde BuscaCursos UC, \
        creada para el funcionamiento de https://www.horariomaker.com.",
    version="4.0.0",
)
app.include_router(MainRouter)
