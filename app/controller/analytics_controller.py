from typing import Dict, List

from fastapi import APIRouter, Depends, Request

from app.models.url import URLResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/urls", response_model=List[URLResponse])
async def get_most_clicked_urls(
    request: Request,
    limit: int = 10,
    analytics_service: AnalyticsService = Depends(),
) -> List[URLResponse]:
    """
    Get the most clicked URLs, ordered by number of clicks (descending)
    """
    return await analytics_service.get_most_clicked_urls(request, limit)


@router.get("/summary", response_model=Dict[str, int])
async def get_analytics_summary(
    analytics_service: AnalyticsService = Depends(),
) -> Dict[str, int]:
    """
    Get a summary of analytics data:
    - Total URLs
    - Total clicks
    - Total custom URLs
    """
    return await analytics_service.get_analytics_summary()
