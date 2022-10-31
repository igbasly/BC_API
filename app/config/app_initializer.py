from fastapi.middleware.cors import CORSMiddleware


app_configuration = {
    "title": "BuscaCursos UC API",
    "description": "REST API para obtener información desde BuscaCursos UC, \
        creada para el funcionamiento de https://www.horariomaker.com.",
    "openapi_tags": [
        {
            "name": "Home",
            "description": "Main endpoints to get basic information.",
        },
        {
            "name": "UC",
            "description": "Endpoint asociated to https://buscacursos.uc.cl to\
                 get everything you need about UC courses.",
        },
    ],
    "docs_url": None,
    "redoc_url": "/documentation",
    "version": "4.0.0"
}

allowed_origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://bc.horariomaker.com",
    "https://horariomaker.com",
    "*"
]

app_middlewares = [
    {
        "middleware_class": CORSMiddleware,
        "allow_origins": allowed_origins,
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
]
