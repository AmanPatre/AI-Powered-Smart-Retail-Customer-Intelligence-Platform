"""Pydantic request and response schemas for Sentiment Analysis module."""

from typing import Optional, Dict
from pydantic import BaseModel, Field


class SentimentRequest(BaseModel):
    review_text: str = Field(..., min_length=2, example="The product quality was amazing and delivery was super fast!")
    customer_id: Optional[int] = Field(None, example=1)


class SentimentResponse(BaseModel):
    sentiment: str = Field(..., example="Positive", description="Predicted sentiment label (Positive, Neutral, Negative)")
    confidence: float = Field(..., example=0.92, description="Prediction probability confidence")
    probabilities: Dict[str, float] = Field(..., description="Probability breakdown across Positive, Neutral, Negative")
    cleaned_text: str = Field(..., description="Preprocessed review text used for model inference")
    review_id: Optional[int] = Field(None, description="Database review record ID")
