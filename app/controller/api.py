from fastapi import APIRouter

from app.controller import url_controller

api_router = APIRouter()


api_router.include_router(url_controller.router, prefix="/urls", tags=["urls"])
