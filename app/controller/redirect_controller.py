from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.services.url_service import URLService

router = APIRouter()


@router.get("/{short_code}")
async def redirect_to_url(
    short_code: str, request: Request, url_service: URLService = Depends()
):
    """
    Root-level redirect for shortened URLs
    """
    original_url = await url_service.get_original_url(short_code, request)
    return RedirectResponse(url=original_url)
