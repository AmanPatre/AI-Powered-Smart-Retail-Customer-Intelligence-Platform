"""Pydantic request and response schemas for FAQ Chatbot module."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, example="What are your store operating hours?")


class ChatResponse(BaseModel):
    response: str = Field(..., example="Our stores are open Mon-Sat 8AM-10PM and Sun 9AM-8PM.")
    intent: str = Field(..., example="store_hours", description="Identified dialogue intent tag")
    confidence: float = Field(..., example=0.98, description="Intent classification confidence score")
    log_id: int = Field(..., description="ID of database chat log entry")
