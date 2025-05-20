from datetime import datetime
from typing import Optional

from pydantic import HttpUrl
from sqlmodel import Field, SQLModel


class URL(SQLModel, table=True):
    """URL model for database"""

    __tablename__ = "urls"

    id: int = Field(default=None, primary_key=True)
    original_url: str = Field(index=True)
    short_code: str = Field(unique=True, index=True)
    is_custom: bool = Field(default=False)
    clicks: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    is_deleted: bool = Field(default=False)


# DTOs
class URLCreate(SQLModel):
    original_url: HttpUrl
    custom_alias: Optional[str] = None


class URLUpdate(SQLModel):
    original_url: Optional[HttpUrl] = None


class URLResponse(SQLModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    is_custom: bool
    clicks: int
    created_at: datetime
    updated_at: Optional[datetime] = None
