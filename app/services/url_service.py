import asyncio
import random
import re
import string
from datetime import datetime
from typing import List

from fastapi import Depends, HTTPException, Request, status

from app.database.url_repository import URLRepository
from app.models.url import URL, URLCreate, URLResponse, URLUpdate


class URLService:
    def __init__(self, url_repository: URLRepository = Depends()):
        self.url_repository = url_repository
        self.code_length = 6

    async def get_all_urls(
        self, request: Request, skip: int = 0, limit: int = 100
    ) -> List[URLResponse]:
        urls = await self.url_repository.get_all(skip=skip, limit=limit)
        base_url = str(request.base_url)
        return await asyncio.gather(
            *[self._create_url_response(url, base_url) for url in urls]
        )

    async def create_short_url(
        self, url_create: URLCreate, request: Request
    ) -> URLResponse:
        existing_url = await self.url_repository.get_by_original_url(
            str(url_create.original_url)
        )

        if existing_url and not url_create.custom_alias:
            base_url = str(request.base_url)
            return await self._create_url_response(existing_url, base_url)

        if url_create.custom_alias:
            if not self._is_valid_custom_alias(url_create.custom_alias):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Custom alias must be alphanumeric and between 4-20 characters",
                )

            exists = await self.url_repository.exists_by_short_code(
                url_create.custom_alias
            )
            if exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Custom alias already in use",
                )

            short_code = url_create.custom_alias
            is_custom = True
        else:
            short_code = await self._generate_short_code()
            is_custom = False

        url_db = URL.model_validate(
            {
                "original_url": str(url_create.original_url),
                "short_code": short_code,
                "is_custom": is_custom,
                "created_at": datetime.utcnow(),
            }
        )

        created_url = await self.url_repository.create(url_db)

        base_url = str(request.base_url)
        return await self._create_url_response(created_url, base_url)

    def _is_valid_custom_alias(self, alias: str) -> bool:
        if not 4 <= len(alias) <= 20:
            return False

        return bool(re.match(r"^[a-zA-Z0-9_]+$", alias))

    async def get_short_url(self, short_code: str, request: Request) -> URLResponse:
        url_db = await self._get_url_by_short_code(short_code)
        base_url = str(request.base_url)
        return await self._create_url_response(url_db, base_url)

    async def update_short_url(
        self, short_code: str, url_update: URLUpdate, request: Request
    ) -> URLResponse:
        url_db = await self._get_url_by_short_code(short_code)

        if url_update.original_url:
            url_db.original_url = str(url_update.original_url)

        updated_url = await self.url_repository.update(url_db)
        base_url = str(request.base_url)
        return await self._create_url_response(updated_url, base_url)

    async def delete_short_url(self, short_code: str, request: Request) -> URLResponse:
        url_db = await self._get_url_by_short_code(short_code)
        deleted_url = await self.url_repository.delete(url_db)
        base_url = str(request.base_url)
        return await self._create_url_response(deleted_url, base_url)

    async def get_original_url(self, short_code: str, request: Request) -> str:
        url_db = await self._get_url_by_short_code(short_code)

        url_db.clicks += 1
        await self.url_repository.update(url_db)

        return url_db.original_url

    async def _get_url_by_short_code(self, short_code: str) -> URL:
        url_db = await self.url_repository.get_by_short_code(short_code)

        if not url_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
            )
        return url_db

    async def _generate_short_code(self) -> str:
        async with self.url_repository.transaction():
            while True:
                chars = string.ascii_letters + string.digits
                short_code = "".join(
                    random.choice(chars) for _ in range(self.code_length)
                )

                exists = await self.url_repository.exists_by_short_code(short_code)

                if not exists:
                    return short_code

    async def _create_url_response(self, url_db: URL, base_url: str) -> URLResponse:
        return URLResponse(
            id=url_db.id,
            original_url=url_db.original_url,
            short_code=url_db.short_code,
            short_url=f"{base_url}{url_db.short_code}",
            is_custom=url_db.is_custom,
            clicks=url_db.clicks,
            created_at=url_db.created_at,
            updated_at=url_db.updated_at,
        )
