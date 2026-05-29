from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

class Security(BaseModel):
    is_protected: bool = False
    password: Optional[str] = None
    is_burn_after_read: bool = False

class Stats(BaseModel):
    views: int = 0
    downloads: int = 0

class Timestamps(BaseModel):
    created_at: str
    expires_at: Optional[str] = None

class PasteCreate(BaseModel):
    title: str = ""
    content: str
    syntax: str = "text"

    security: Security = Field(
        default_factory=Security
    )

    is_expiry: bool = False
    expiry_date: Optional[date] = None
    expiry_hour: Optional[int] = Field(
        default=None,
        ge=0,
        le=23,
    )
    expiry_minute: Optional[int] = Field(
        default=None,
        ge=0,
        le=59,
    )
    tz_offset_minutes: Optional[int] = Field(default=0)

    @property
    def is_protected(self) -> bool:
        return self.security.is_protected

    @property
    def password(self) -> Optional[str]:
        return self.security.password

    @property
    def is_burn_after_read(self) -> bool:
        return self.security.is_burn_after_read

class PasteResponse(BaseModel):
    id: str
    title: str
    content: str
    syntax: str
    is_protected: bool
    is_burn_after_read: bool
    security: Security
    stats: Stats
    timestamps: Timestamps
    views: int
    downloads: int
    created_at: str
    expires_at: Optional[str] = None
    url: str
