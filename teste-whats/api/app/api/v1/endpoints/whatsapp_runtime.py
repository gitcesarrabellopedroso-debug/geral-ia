from fastapi import APIRouter, Header, HTTPException, Query, status

from app.clients.whatsapp_bridge import WhatsAppBridgeClient
from app.core.config import get_settings
from app.core.database import get_database
from app.repositories.whatsapp_session_repository import WhatsAppSessionRepository
from app.schemas.whatsapp_session import (
    WhatsAppBridgeWebhookPayload,
    WhatsAppRuntimeResponse,
    WhatsAppSendMessageRequest,
    WhatsAppSendMessageResponse,
)
from app.services.whatsapp_runtime_service import WhatsAppRuntimeService

router = APIRouter()


def get_runtime_service() -> WhatsAppRuntimeService:
    settings = get_settings()
    repository = WhatsAppSessionRepository(get_database())
    bridge_client = WhatsAppBridgeClient(settings)
    return WhatsAppRuntimeService(repository, bridge_client, settings)


def validate_bridge_api_key(x_api_key: str | None) -> None:
    settings = get_settings()
    if settings.whatsapp_bridge_api_key and x_api_key != settings.whatsapp_bridge_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bridge API key.",
        )


@router.get("/status", response_model=WhatsAppRuntimeResponse)
async def get_whatsapp_runtime_status(
    session_key: str | None = Query(default=None),
) -> WhatsAppRuntimeResponse:
    service = get_runtime_service()
    return await service.get_runtime_status(session_key=session_key)


@router.post("/session/start", response_model=WhatsAppRuntimeResponse)
async def start_whatsapp_runtime_session(
    session_key: str | None = Query(default=None),
) -> WhatsAppRuntimeResponse:
    service = get_runtime_service()
    try:
        return await service.start_runtime_session(session_key=session_key)
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc


@router.post("/session/disconnect", response_model=WhatsAppRuntimeResponse)
async def disconnect_whatsapp_runtime_session(
    session_key: str | None = Query(default=None),
) -> WhatsAppRuntimeResponse:
    service = get_runtime_service()
    try:
        return await service.disconnect_runtime_session(session_key=session_key)
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc


@router.post("/webhooks/session-events", response_model=WhatsAppRuntimeResponse)
async def handle_whatsapp_runtime_event(
    payload: WhatsAppBridgeWebhookPayload,
    x_api_key: str | None = Header(default=None),
) -> WhatsAppRuntimeResponse:
    validate_bridge_api_key(x_api_key)
    service = get_runtime_service()
    return await service.sync_runtime_event(payload)


@router.post("/messages/send", response_model=WhatsAppSendMessageResponse)
async def send_whatsapp_message(
    payload: WhatsAppSendMessageRequest,
) -> WhatsAppSendMessageResponse:
    service = get_runtime_service()
    try:
        return await service.send_runtime_message(
            session_key=payload.session_key,
            phone=payload.phone,
            text=payload.text,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
