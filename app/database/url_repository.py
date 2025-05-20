from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncContextManager, List, Optional

from fastapi import Depends
from sqlmodel import Session, select

from app.database.db import get_db
from app.models.url import URL


class URLRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    @asynccontextmanager
    async def transaction(self) -> AsyncContextManager[None]:  # type: ignore
        """
        Provides a transaction context to ensure atomicity
        """
        try:
            # Only start a new transaction if one is not already in progress
            if not self.db.in_transaction():
                with self.db.begin() as transaction:
                    yield
            else:
                # If already in a transaction, just yield control
                yield
        except Exception:
            # Transaction will be rolled back automatically by the context manager
            raise

    async def get_all(
        self, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> List[URL]:
        statement = select(URL).offset(skip).limit(limit)
        if not include_deleted:
            statement = statement.where(URL.is_deleted == False)  # noqa: E712
        result = self.db.exec(statement)
        return result.all()

    async def get_by_short_code(
        self, short_code: str, include_deleted: bool = False
    ) -> Optional[URL]:
        statement = select(URL).where(URL.short_code == short_code)
        if not include_deleted:
            statement = statement.where(URL.is_deleted == False)  # noqa: E712
        result = self.db.exec(statement)
        return result.first()

    async def get_by_original_url(
        self, original_url: str, include_deleted: bool = False
    ) -> Optional[URL]:
        statement = select(URL).where(URL.original_url == original_url)
        if not include_deleted:
            statement = statement.where(URL.is_deleted == False)  # noqa: E712
        result = self.db.exec(statement)
        return result.first()

    async def create(self, url: URL) -> URL:
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)
        return url

    async def update(self, url: URL) -> URL:
        url.updated_at = datetime.utcnow()
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)
        return url

    async def delete(self, url: URL) -> URL:
        url.is_deleted = True
        url.updated_at = datetime.utcnow()
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)
        return url

    async def exists_by_short_code(
        self, short_code: str, include_deleted: bool = False
    ) -> bool:
        result = await self.get_by_short_code(short_code, include_deleted)
        return result is not None
