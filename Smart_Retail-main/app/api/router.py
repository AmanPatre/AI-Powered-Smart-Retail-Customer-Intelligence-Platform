"""Aggregated API router incorporating all module endpoints."""

from fastapi import APIRouter
from app.api import (
    health,
    face_routes,
    product_routes,
    sentiment_routes,
    chatbot_routes,
    dashboard_routes,
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(face_routes.router)
api_router.include_router(product_routes.router)
api_router.include_router(sentiment_routes.router)
api_router.include_router(chatbot_routes.router)
api_router.include_router(dashboard_routes.router)
