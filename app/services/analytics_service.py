import asyncio
from typing import Dict, List

from fastapi import Depends, Request

from app.database.url_repository import URLRepository
from app.models.url import URLResponse
from app.services.url_service import URLService


class AnalyticsService:
    def __init__(
        self,
        url_repository: URLRepository = Depends(),
        url_service: URLService = Depends(),
    ):
        self.url_repository = url_repository
        self.url_service = url_service

    async def get_most_clicked_urls(
        self, request: Request, limit: int = 10
    ) -> List[URLResponse]:
        urls = self.url_repository.get_most_clicked(limit=limit)
        base_url = str(request.base_url)
        return await asyncio.gather(
            *[self.url_service._create_url_response(url, base_url) for url in urls]
        )

    async def get_analytics_summary(self) -> Dict[str, int]:
        total_urls = self.url_repository.count_urls()
        total_clicks = self.url_repository.count_total_clicks()
        total_custom_urls = self.url_repository.count_custom_urls()

        return {
            "total_urls": total_urls,
            "total_clicks": total_clicks,
            "total_custom_urls": total_custom_urls,
        }
