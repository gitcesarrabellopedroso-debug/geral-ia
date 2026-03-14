from fastapi import APIRouter

from app.core.config import get_settings
from app.core.database import get_database
from app.schemas.whatsapp_session import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def healthcheck() -> HealthResponse:
    settings = get_settings()
    database = get_database()
    await database.command("ping")
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        environment=settings.app_env,
        mongodb="ok",
    )
