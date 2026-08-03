"""Pydantic schemas for Dashboard statistics endpoint."""

from typing import Dict, List, Any
from pydantic import BaseModel, Field


class DashboardStatsResponse(BaseModel):
    total_customers: int = Field(..., example=42)
    total_visits: int = Field(..., example=156)
    total_reviews: int = Field(..., example=89)
    total_chat_queries: int = Field(..., example=210)
    sentiment_breakdown: Dict[str, int] = Field(..., example={"Positive": 54, "Neutral": 20, "Negative": 15})
    top_intents: Dict[str, int] = Field(..., example={"store_hours": 45, "return_policy": 32})
    recent_visits: List[Dict[str, Any]] = Field(...)
    recent_reviews: List[Dict[str, Any]] = Field(...)
    system_status: str = Field(..., example="Operational")
