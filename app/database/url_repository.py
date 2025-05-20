from datetime import datetime
from typing import Optional

from fastapi import Depends
from sqlmodel import Session, select

from app.database.db import get_db
from app.models.url import URL


class URLRepository:
    """Repository for URL database operations"""

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_by_short_code(
        self, short_code: str, include_deleted: bool = False
    ) -> Optional[URL]:
        """Get URL by short code"""
        statement = select(URL).where(URL.short_code == short_code)
        if not include_deleted:
            statement = statement.where(URL.is_deleted == False)
        return self.db.exec(statement).first()

    def get_by_original_url(
        self, original_url: str, include_deleted: bool = False
    ) -> Optional[URL]:
        """Get URL by original URL"""
        statement = select(URL).where(URL.original_url == original_url)
        if not include_deleted:
            statement = statement.where(URL.is_deleted == False)
        return self.db.exec(statement).first()

    def create(self, url: URL) -> URL:
        """Create a new URL"""
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)
        return url

    def update(self, url: URL) -> URL:
        """Update an existing URL"""
        url.updated_at = datetime.utcnow()
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)
        return url

    def delete(self, url: URL) -> URL:
        """Delete a URL"""
        url.is_deleted = True
        url.updated_at = datetime.utcnow()
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)
        return url

    def exists_by_short_code(
        self, short_code: str, include_deleted: bool = False
    ) -> bool:
        """Check if a URL with the given short code exists"""
        return self.get_by_short_code(short_code, include_deleted) is not None
