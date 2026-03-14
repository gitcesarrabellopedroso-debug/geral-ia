from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException, Query, status

from app.core.database import get_database
from app.repositories.whatsapp_session_repository import WhatsAppSessionRepository
from app.schemas.whatsapp_session import (
    WhatsAppSessionCreate,
    WhatsAppSessionInDB,
    WhatsAppSessionListResponse,
    WhatsAppSessionUpdate,
)

router = APIRouter()


@router.post("", response_model=WhatsAppSessionInDB, status_code=status.HTTP_201_CREATED)
async def create_whatsapp_session(payload: WhatsAppSessionCreate) -> WhatsAppSessionInDB:
    repository = WhatsAppSessionRepository(get_database())
    try:
        document = await repository.create(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return WhatsAppSessionInDB.model_validate(document)


@router.get("", response_model=WhatsAppSessionListResponse)
async def list_whatsapp_sessions(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
) -> WhatsAppSessionListResponse:
    repository = WhatsAppSessionRepository(get_database())
    items, total = await repository.list(skip=skip, limit=limit)
    return WhatsAppSessionListResponse(
        items=[WhatsAppSessionInDB.model_validate(item) for item in items],
        total=total,
    )


@router.get("/{session_id}", response_model=WhatsAppSessionInDB)
async def get_whatsapp_session(session_id: str) -> WhatsAppSessionInDB:
    repository = WhatsAppSessionRepository(get_database())

    try:
        document = await repository.get(session_id)
    except InvalidId as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid session id.") from exc

    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

    return WhatsAppSessionInDB.model_validate(document)


@router.patch("/{session_id}", response_model=WhatsAppSessionInDB)
async def update_whatsapp_session(session_id: str, payload: WhatsAppSessionUpdate) -> WhatsAppSessionInDB:
    repository = WhatsAppSessionRepository(get_database())

    try:
        document = await repository.update(session_id, payload)
    except InvalidId as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid session id.") from exc

    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

    return WhatsAppSessionInDB.model_validate(document)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_whatsapp_session(session_id: str) -> None:
    repository = WhatsAppSessionRepository(get_database())

    try:
        deleted = await repository.delete(session_id)
    except InvalidId as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid session id.") from exc

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
