from datetime import datetime
from typing import List, Optional

from fastapi import Depends
from sqlmodel import Session, func, select

from app.database.db import get_db
from app.models.url import URL


class URLRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[URL]:
        statement = select(URL).offset(skip).limit(limit).where(URL.is_deleted == False)  # noqa: E712
        result = self.db.exec(statement)
        return result.all()

    def get_by_short_code(self, short_code: str) -> Optional[URL]:
        statement = (
            select(URL)
            .where(URL.short_code == short_code)
            .where(URL.is_deleted == False)  # noqa: E712
        )
        result = self.db.exec(statement)
        return result.first()

    def get_by_original_url(self, original_url: str) -> Optional[URL]:
        statement = (
            select(URL)
            .where(URL.original_url == original_url)
            .where(URL.is_deleted == False)
        )  # noqa: E712
        result = self.db.exec(statement)
        return result.first()

    def create(self, url: URL) -> URL:
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)
        return url

    def update(self, url: URL) -> URL:
        url.updated_at = datetime.utcnow()
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)
        return url

    def delete(self, url: URL) -> URL:
        url.is_deleted = True
        url.updated_at = datetime.utcnow()
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)
        return url

    def exists_by_short_code(self, short_code: str) -> bool:
        result = self.get_by_short_code(short_code)
        return result is not None

    # Analytics methods

    def get_most_clicked(self, limit: int = 10) -> List[URL]:
        """
        Get URLs ordered by click count (descending)
        """
        statement = (
            select(URL)
            .order_by(URL.clicks.desc())
            .limit(limit)
            .where(URL.is_deleted == False)  # noqa: E712
        )
        result = self.db.exec(statement)
        return result.all()

    def count_urls(self) -> int:
        """
        Count total number of URLs
        """
        statement = select(func.count(URL.id)).where(URL.is_deleted == False)  # noqa: E712
        result = self.db.exec(statement)
        return result.first() or 0

    def count_total_clicks(self) -> int:
        """
        Count total number of clicks across all URLs
        """
        statement = select(func.sum(URL.clicks)).where(URL.is_deleted == False)  # noqa: E712
        result = self.db.exec(statement)
        return result.first() or 0

    def count_custom_urls(self) -> int:
        """
        Count number of custom URLs
        """
        statement = (
            select(func.count(URL.id))
            .where(URL.is_custom == True)
            .where(URL.is_deleted == False)
        )  # noqa: E712
        result = self.db.exec(statement)
        return result.first() or 0
