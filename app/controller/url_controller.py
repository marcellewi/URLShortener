from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse

from app.models.url import URLCreate, URLResponse, URLUpdate
from app.services.url_service import URLService

router = APIRouter()


@router.post(
    "/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED
)
async def create_short_url(
    url_create: URLCreate, request: Request, url_service: URLService = Depends()
) -> URLResponse:
    """
    Create a shortened URL
    """
    return url_service.create_short_url(url_create, request)


@router.get(
    "/{short_code}",
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def redirect_to_url(
    short_code: str, request: Request, url_service: URLService = Depends()
) -> RedirectResponse:
    """
    Redirect to the original URL
    """
    original_url = url_service.get_original_url(short_code, request)
    return RedirectResponse(url=original_url)


@router.get("/{short_code}/stats", response_model=URLResponse)
async def get_url_stats(
    short_code: str, request: Request, url_service: URLService = Depends()
) -> URLResponse:
    """
    Get statistics for a shortened URL
    """
    return url_service.get_url_stats(short_code, request)


@router.get("/api/{short_code}", response_model=URLResponse)
async def get_short_url(
    short_code: str, request: Request, url_service: URLService = Depends()
) -> URLResponse:
    """
    Get a short URL by its code without redirecting or incrementing clicks
    """
    return url_service.get_short_url(short_code, request)


@router.put("/api/{short_code}", response_model=URLResponse)
async def update_short_url(
    short_code: str,
    url_update: URLUpdate,
    request: Request,
    url_service: URLService = Depends(),
) -> URLResponse:
    """
    Update a short URL
    """
    return url_service.update_short_url(short_code, url_update, request)


@router.delete("/api/{short_code}")
async def delete_short_url(
    short_code: str, request: Request, url_service: URLService = Depends()
) -> URLResponse:
    """
    Delete a short URL
    """
    return url_service.delete_short_url(short_code, request)
