"""Pydantic request and response schemas for Face Recognition module."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class CustomerBase(BaseModel):
    name: str = Field(..., example="Jane Doe")
    email: Optional[str] = Field(None, example="jane.doe@example.com")


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FaceRecognitionResponse(BaseModel):
    recognized: bool = Field(..., description="Whether a returning customer was identified")
    customer: Optional[CustomerResponse] = Field(None, description="Matched customer profile if recognized")
    confidence: float = Field(..., description="Match confidence score between 0.0 and 1.0")
    visit_id: Optional[int] = Field(None, description="ID of newly logged visit record")
    faces_detected: int = Field(..., description="Total number of faces detected in uploaded image")
    message: str = Field(..., description="Status summary message")
