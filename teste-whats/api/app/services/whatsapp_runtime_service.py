from datetime import datetime
from typing import Any

from app.clients.whatsapp_bridge import (
    WhatsAppBridgeClient,
    WhatsAppBridgeError,
    WhatsAppBridgeNotConfiguredError,
)
from app.core.config import Settings
from app.repositories.whatsapp_session_repository import WhatsAppSessionRepository
from app.schemas.whatsapp_session import WhatsAppBridgeWebhookPayload, WhatsAppRuntimeResponse


class WhatsAppRuntimeService:
    def __init__(
        self,
        repository: WhatsAppSessionRepository,
        bridge_client: WhatsAppBridgeClient,
        settings: Settings,
    ) -> None:
        self.repository = repository
        self.bridge_client = bridge_client
        self.settings = settings

    async def get_runtime_status(self, session_key: str | None = None) -> WhatsAppRuntimeResponse:
        normalized_key = self._get_session_key(session_key)

        try:
            bridge_payload = await self.bridge_client.get_status(normalized_key)
            document = await self._sync_bridge_payload(normalized_key, bridge_payload)
        except WhatsAppBridgeNotConfiguredError:
            document = await self.repository.get_by_session_key(normalized_key)
            if document is None:
                return self._build_runtime_response(
                    session_key=normalized_key,
                    status="offline",
                    last_error="bridge_not_configured",
                )
        except WhatsAppBridgeError as exc:
            document = await self._save_error_state(normalized_key, str(exc))

        return self._document_to_runtime(document)

    async def start_runtime_session(self, session_key: str | None = None) -> WhatsAppRuntimeResponse:
        normalized_key = self._get_session_key(session_key)

        try:
            bridge_payload = await self.bridge_client.start_session(normalized_key)
        except WhatsAppBridgeNotConfiguredError as exc:
            raise RuntimeError("WhatsApp bridge is not configured.") from exc
        except WhatsAppBridgeError as exc:
            document = await self._save_error_state(normalized_key, str(exc))
            return self._document_to_runtime(document)

        document = await self._sync_bridge_payload(normalized_key, bridge_payload)
        return self._document_to_runtime(document)

    async def disconnect_runtime_session(self, session_key: str | None = None) -> WhatsAppRuntimeResponse:
        normalized_key = self._get_session_key(session_key)

        try:
            bridge_payload = await self.bridge_client.disconnect_session(normalized_key)
        except WhatsAppBridgeNotConfiguredError as exc:
            raise RuntimeError("WhatsApp bridge is not configured.") from exc
        except WhatsAppBridgeError as exc:
            document = await self._save_error_state(normalized_key, str(exc))
            return self._document_to_runtime(document)

        document = await self._sync_bridge_payload(normalized_key, bridge_payload)
        return self._document_to_runtime(document)

    async def sync_runtime_event(self, payload: WhatsAppBridgeWebhookPayload) -> WhatsAppRuntimeResponse:
        document = await self.repository.upsert_by_session_key(
            payload.session_key,
            {
                "status": payload.status,
                "phone": payload.phone,
                "provider_session_id": payload.provider_session_id,
                "qr_token": payload.qr_token,
                "qr_image_data_url": payload.qr_image_data_url,
                "last_error": payload.last_error,
                "metadata": payload.metadata,
            },
        )
        return self._document_to_runtime(document)

    def _get_session_key(self, session_key: str | None) -> str:
        return (session_key or self.settings.whatsapp_default_session_key).strip().lower()

    async def _sync_bridge_payload(self, session_key: str, payload: dict[str, Any]) -> dict:
        document = await self.repository.upsert_by_session_key(
            session_key,
            {
                "status": payload.get("status", "offline"),
                "phone": payload.get("phone"),
                "provider_session_id": payload.get("provider_session_id") or payload.get("providerSessionId") or payload.get("session_id") or payload.get("sessionId"),
                "qr_token": payload.get("qr_token") or payload.get("qrToken"),
                "qr_image_data_url": payload.get("qr_image_data_url") or payload.get("qrImageDataUrl"),
                "last_error": payload.get("last_error") or payload.get("lastError"),
                "metadata": payload.get("metadata", {}),
            },
        )
        return document

    async def _save_error_state(self, session_key: str, message: str) -> dict:
        return await self.repository.upsert_by_session_key(
            session_key,
            {
                "status": "error",
                "last_error": message,
                "metadata": {},
            },
        )

    def _document_to_runtime(self, document: dict | None) -> WhatsAppRuntimeResponse:
        if not document:
            return self._build_runtime_response(
                session_key=self.settings.whatsapp_default_session_key,
                status="offline",
            )

        return self._build_runtime_response(
            session_id=document.get("provider_session_id") or document.get("id"),
            session_key=document["session_key"],
            status=document["status"],
            phone=document.get("phone"),
            qr_token=document.get("qr_token"),
            qr_image_data_url=document.get("qr_image_data_url"),
            provider_session_id=document.get("provider_session_id"),
            last_error=document.get("last_error"),
            metadata=document.get("metadata", {}),
            updated_at=document.get("updated_at"),
        )

    def _build_runtime_response(
        self,
        *,
        session_key: str,
        status: str,
        session_id: str | None = None,
        phone: str | None = None,
        qr_token: str | None = None,
        qr_image_data_url: str | None = None,
        provider_session_id: str | None = None,
        last_error: str | None = None,
        metadata: dict[str, Any] | None = None,
        updated_at: datetime | None = None,
    ) -> WhatsAppRuntimeResponse:
        return WhatsAppRuntimeResponse(
            session_id=session_id,
            session_key=session_key,
            status=status,
            phone=phone,
            qr_token=qr_token,
            qr_image_data_url=qr_image_data_url,
            provider_session_id=provider_session_id,
            last_error=last_error,
            metadata=metadata or {},
            updated_at=updated_at,
        )
