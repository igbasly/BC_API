# Intializers FIRST
from .assets_initializer import load_manifest
from .app_initializer import (
    app_configuration as AppConfiguration,
    app_middlewares as AppMiddlewares
)

# Routes and other configs after
from .routes import main_router as MainRouter
