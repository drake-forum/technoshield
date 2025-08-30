from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.alerts import router as alerts_router
from app.api.routes.incidents import router as incidents_router
from app.api.routes.users import router as users_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(alerts_router, prefix="/alerts", tags=["alerts"])
api_router.include_router(incidents_router, prefix="/incidents", tags=["incidents"])
api_router.include_router(users_router, prefix="/users", tags=["users"])