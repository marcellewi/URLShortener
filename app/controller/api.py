from fastapi import APIRouter

from app.controller import analytics_controller, url_controller

api_router = APIRouter()


api_router.include_router(url_controller.router, prefix="/urls", tags=["urls"])
api_router.include_router(
    analytics_controller.router, prefix="/analytics", tags=["analytics"]
)
