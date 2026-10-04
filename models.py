from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, model_validator

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
    title: str = Field(default="", max_length=200)
    content: str = Field(..., min_length=1, max_length=1_000_000)
    syntax: str = Field(default="text", max_length=50)

    security: Security = Field(default_factory=Security)
    password: Optional[str] = Field(default=None, max_length=128)
    is_burn_after_read: Optional[bool] = None

    is_expiry: bool = False
    expiry_date: Optional[date] = None
    expiry_hour: Optional[int] = Field(default=None, ge=0, le=23)
    expiry_minute: Optional[int] = Field(default=None, ge=0, le=59)
    expires_in_hours: Optional[int] = Field(default=None, ge=1, le=8760)
    tz_offset_minutes: Optional[int] = Field(default=0)

    @model_validator(mode="after")
    def sync_security_fields(self):
        # Sync top-level password with security sub-model
        if self.password:
            self.security.password = self.password
            self.security.is_protected = True
        elif self.security.password:
            self.security.is_protected = True

        # Sync burn_after_read
        if self.is_burn_after_read is not None:
            self.security.is_burn_after_read = self.is_burn_after_read

        return self

    @property
    def is_protected(self) -> bool:
        return self.security.is_protected or bool(self.security.password)

    @property
    def effective_password(self) -> Optional[str]:
        return self.security.password or self.password

    @property
    def burn_after_read(self) -> bool:
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
