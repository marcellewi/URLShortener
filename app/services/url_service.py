import random
import string
from datetime import datetime

from fastapi import Depends, HTTPException, Request, status

from app.database.url_repository import URLRepository
from app.models.url import URL, URLCreate, URLResponse, URLUpdate


class URLService:
    def __init__(self, url_repository: URLRepository = Depends()):
        self.url_repository = url_repository
        self.code_length = 6

    def create_short_url(self, url_create: URLCreate, request: Request) -> URLResponse:
        existing_url = self.url_repository.get_by_original_url(
            str(url_create.original_url)
        )

        if existing_url:
            base_url = str(request.base_url)
            return self._create_url_response(existing_url, base_url)

        short_code = self._generate_short_code()

        url_db = URL.model_validate(
            {
                "original_url": str(url_create.original_url),
                "short_code": short_code,
                "created_at": datetime.utcnow(),
            }
        )

        created_url = self.url_repository.create(url_db)

        base_url = str(request.base_url)
        return self._create_url_response(created_url, base_url)

    def get_short_url(self, short_code: str, request: Request) -> URLResponse:
        """
        Get a shortened URL by short code without incrementing clicks
        """
        url_db = self._get_url_by_short_code(short_code)
        base_url = str(request.base_url)
        return self._create_url_response(url_db, base_url)

    def update_short_url(
        self, short_code: str, url_update: URLUpdate, request: Request
    ) -> URLResponse:
        """
        Update a shortened URL
        """
        url_db = self._get_url_by_short_code(short_code)

        if url_update.original_url:
            url_db.original_url = str(url_update.original_url)

        updated_url = self.url_repository.update(url_db)
        base_url = str(request.base_url)
        return self._create_url_response(updated_url, base_url)

    def delete_short_url(self, short_code: str, request: Request) -> URLResponse:
        """
        Soft delete a shortened URL by marking it as deleted
        """
        url_db = self._get_url_by_short_code(short_code)
        deleted_url = self.url_repository.delete(url_db)
        base_url = str(request.base_url)
        return self._create_url_response(deleted_url, base_url)

    def get_original_url(self, short_code: str, request: Request) -> str:
        """
        Get the original URL from a short code and increment click counter
        """
        url_db = self._get_url_by_short_code(short_code)

        url_db.clicks += 1
        self.url_repository.update(url_db)

        return url_db.original_url

    def get_url_stats(self, short_code: str, request: Request) -> URLResponse:
        """
        Get statistics for a shortened URL
        """
        url_db = self._get_url_by_short_code(short_code)
        base_url = str(request.base_url)
        return self._create_url_response(url_db, base_url)

    def _get_url_by_short_code(self, short_code: str) -> URL:
        """
        Get URL by short code or raise 404
        """
        url_db = self.url_repository.get_by_short_code(short_code)

        if not url_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
            )
        return url_db

    def _generate_short_code(self) -> str:
        """
        Generate a unique short code
        """
        while True:
            chars = string.ascii_letters + string.digits
            short_code = "".join(random.choice(chars) for _ in range(self.code_length))

            exists = self.url_repository.exists_by_short_code(short_code)

            if not exists:
                return short_code

    def _create_url_response(self, url_db: URL, base_url: str) -> URLResponse:
        return URLResponse(
            id=url_db.id,
            original_url=url_db.original_url,
            short_code=url_db.short_code,
            short_url=f"{base_url}{url_db.short_code}",
            clicks=url_db.clicks,
            created_at=url_db.created_at,
            updated_at=url_db.updated_at,
            is_deleted=url_db.is_deleted,
        )
