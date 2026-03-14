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
    provider_session_id: str | None = Field(default=None, max_length=120)
    qr_token: str | None = Field(default=None, max_length=2048)
    qr_image_data_url: str | None = Field(default=None, max_length=400000)
    last_error: str | None = Field(default=None, max_length=500)
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
    provider_session_id: str | None = Field(default=None, max_length=120)
    qr_token: str | None = Field(default=None, max_length=2048)
    qr_image_data_url: str | None = Field(default=None, max_length=400000)
    last_error: str | None = Field(default=None, max_length=500)
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


class WhatsAppRuntimeResponse(APIModel):
    session_id: str | None = None
    session_key: str
    status: SessionStatus
    phone: str | None = None
    qr_token: str | None = None
    qr_image_data_url: str | None = None
    provider_session_id: str | None = None
    last_error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime | None = None


class WhatsAppBridgeWebhookPayload(APIModel):
    session_key: str = Field(min_length=3, max_length=80)
    status: SessionStatus
    phone: str | None = Field(default=None, max_length=32)
    provider_session_id: str | None = Field(default=None, max_length=120)
    qr_token: str | None = Field(default=None, max_length=2048)
    qr_image_data_url: str | None = Field(default=None, max_length=400000)
    last_error: str | None = Field(default=None, max_length=500)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("session_key")
    @classmethod
    def normalize_webhook_session_key(cls, value: str) -> str:
        return value.strip().lower().replace(" ", "-")


class WhatsAppSendMessageRequest(APIModel):
    session_key: str | None = Field(default=None, min_length=3, max_length=80)
    phone: str = Field(min_length=8, max_length=32)
    text: str = Field(min_length=1, max_length=4096)

    @field_validator("session_key")
    @classmethod
    def normalize_session_key(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().lower().replace(" ", "-")


class WhatsAppSendMessageResponse(APIModel):
    session_key: str
    provider_message_id: str | None = None
    to: str
    text: str
    status: str
    metadata: dict[str, Any] = Field(default_factory=dict)
