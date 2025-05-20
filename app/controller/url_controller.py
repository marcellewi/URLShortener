from typing import List

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse

from app.models.url import URLCreate, URLResponse, URLUpdate
from app.services.url_service import URLService

router = APIRouter()


@router.get("/", response_model=List[URLResponse])
async def get_all_urls(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    url_service: URLService = Depends(),
) -> List[URLResponse]:
    return await url_service.get_all_urls(request, skip, limit)


@router.post(
    "/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED
)
async def create_short_url(
    url_create: URLCreate, request: Request, url_service: URLService = Depends()
) -> URLResponse:
    """
    Create a shortened URL
    """
    return await url_service.create_short_url(url_create, request)


@router.get("/{short_code}", response_model=URLResponse)
async def get_short_url(
    short_code: str, request: Request, url_service: URLService = Depends()
) -> URLResponse:
    return await url_service.get_short_url(short_code, request)


@router.put("/{short_code}", response_model=URLResponse)
async def update_short_url(
    short_code: str,
    url_update: URLUpdate,
    request: Request,
    url_service: URLService = Depends(),
) -> URLResponse:
    return await url_service.update_short_url(short_code, url_update, request)


@router.delete("/{short_code}")
async def delete_short_url(
    short_code: str, request: Request, url_service: URLService = Depends()
) -> URLResponse:
    return await url_service.delete_short_url(short_code, request)


@router.get("/r/{short_code}")
async def redirect_to_url(
    short_code: str, request: Request, url_service: URLService = Depends()
) -> RedirectResponse:
    original_url = await url_service.get_original_url(short_code, request)
    return RedirectResponse(url=original_url)
