from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import Field, field_validator

from app.schemas.common import APIModel

SessionStatus = Literal["offline", "awaiting_qr", "connected", "error"]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class WhatsAppSessionBase(APIModel):
    session_key: str = Field(min_length=3, max_length=80)
    status: SessionStatus = "offline"
    phone: str | None = Field(default=None, max_length=32)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("session_key")
    @classmethod
    def normalize_session_key(cls, value: str) -> str:
        return value.strip().lower().replace(" ", "-")


class WhatsAppSessionCreate(WhatsAppSessionBase):
    pass


class WhatsAppSessionUpdate(APIModel):
    status: SessionStatus | None = None
    phone: str | None = Field(default=None, max_length=32)
    metadata: dict[str, Any] | None = None


class WhatsAppSessionInDB(WhatsAppSessionBase):
    id: str
    created_at: datetime
    updated_at: datetime


class WhatsAppSessionListResponse(APIModel):
    items: list[WhatsAppSessionInDB]
    total: int


class HealthResponse(APIModel):
    status: str
    app_name: str
    environment: str
    mongodb: str
