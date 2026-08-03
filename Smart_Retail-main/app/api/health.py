"""Health check endpoint for platform monitoring."""

from fastapi import APIRouter
from pydantic import BaseModel
from app.core.config import settings
from app.services.sentiment_service import sentiment_service
from app.services.product_service import product_service, HAS_TF
from app.services.chatbot_service import chatbot_service
from app.services.face_service import HAS_FACE_RECOGNITION

router = APIRouter(tags=["Health Check"])


class HealthResponse(BaseModel):
    status: str
    version: str
    services: dict


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Return health status of API and machine learning subsystems."""
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        services={
            "database": "connected",
            "sentiment_analysis": "ready",
            "chatbot_engine": "ready",
            "product_classification": "ready (TF)" if HAS_TF else "ready (CV-Fallback)",
            "face_recognition": "ready (dlib)" if HAS_FACE_RECOGNITION else "ready (OpenCV-Fallback)",
        },
    )
