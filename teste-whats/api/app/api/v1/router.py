from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.whatsapp_runtime import router as whatsapp_runtime_router
from app.api.v1.endpoints.whatsapp_sessions import router as whatsapp_sessions_router

router = APIRouter()
router.include_router(health_router, tags=["health"])
router.include_router(whatsapp_sessions_router, prefix="/whatsapp-sessions", tags=["whatsapp-sessions"])
router.include_router(whatsapp_runtime_router, prefix="/whatsapp", tags=["whatsapp-runtime"])
