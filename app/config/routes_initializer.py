import os
from importlib import import_module
from fastapi import APIRouter


def mount_controllers(
    base_router: APIRouter,
    controllers_path: str,
    package: str = "app.controllers"
):
    """ Go over every file and folder inside 'controllers' to automatically
    add them to main_router.

    Args:
        base_router (APIRouter): base instance to add new nested comtrollers.
        controllers_path (str): path to the folder to wallk throgh.
        package (str): relative parent pakage to search new modules.
    """
    controllers_list = os.listdir(controllers_path)
    for path in controllers_list:
        if "__" in path:
            continue

        if '_controller.py' in path:
            controller_name = path.split("_")[0]
            module = import_module(f".{controller_name}_controller", package)
            if hasattr(module, "router"):
                router = module.router
                base_router.include_router(router)

        elif os.path.isdir(os.path.join(controllers_path, path)):
            new_controller_path = os.path.join(controllers_path, path)
            router = APIRouter(prefix=f"/{path}")
            mount_controllers(router, new_controller_path, f"{package}.{path}")
            base_router.include_router(router)


controllers_routes = APIRouter()
controllers_path = os.path.join(".", "app", "controllers")
mount_controllers(controllers_routes, controllers_path)
