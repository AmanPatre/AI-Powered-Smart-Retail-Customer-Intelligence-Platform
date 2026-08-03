"""Pydantic request and response schemas for Product Image Classification module."""

from typing import Dict
from pydantic import BaseModel, Field


class ProductClassificationResponse(BaseModel):
    category: str = Field(..., example="Electronics", description="Predicted retail category")
    confidence: float = Field(..., example=0.965, description="Classification confidence score")
    probabilities: Dict[str, float] = Field(..., description="Probability breakdown across all categories")
    message: str = Field(..., example="Product classified successfully")
