from fastapi import APIRouter
from fastapi.responses import FileResponse

from .routes_initializer import controllers_routes
from ..assets import asset_path


main_router = APIRouter()
main_router.include_router(controllers_routes)

# =============================================================================
# ================ Add new routes to main_router if necessary =================
# ============================= bewllow this line =============================
# =============================================================================


@main_router.get("/favicon.ico", include_in_schema=False)
def favicon_route():
    return FileResponse(asset_path('favicon.png'))
