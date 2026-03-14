from fastapi import APIRouter

from app.api.v1.endpoints.whatsapp_runtime import router as whatsapp_runtime_router
from app.api.v1.router import router as v1_router

api_router = APIRouter()
api_router.include_router(v1_router, prefix="/api/v1")
api_router.include_router(whatsapp_runtime_router, prefix="/api/whatsapp")
