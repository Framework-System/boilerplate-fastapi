from fastapi.routing import APIRouter

from app.api.routes.v1 import auth, monitoring, users

api_router = APIRouter()
api_router.include_router(monitoring.router, prefix="/v1", tags=["health-check"])
api_router.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/v1/users", tags=["users"])
