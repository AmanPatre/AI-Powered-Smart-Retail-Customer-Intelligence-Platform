"""Database entities using SQLAlchemy ORM."""

import json
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Customer(Base):
    """Customer entity holding facial encoding data and metadata."""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=True)
    face_encoding_json = Column(Text, nullable=False)  # JSON-encoded 128d vector
    created_at = Column(DateTime, default=datetime.utcnow)

    visits = relationship("Visit", back_populates="customer", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="customer", cascade="all, delete-orphan")

    def get_face_encoding(self) -> List[float]:
        """Deserialize stored JSON vector back to list of floats."""
        return json.loads(self.face_encoding_json)

    def set_face_encoding(self, encoding: List[float]) -> None:
        """Serialize face encoding list to JSON string."""
        self.face_encoding_json = json.dumps(encoding)


class Visit(Base):
    """Log of every customer store visit captured via camera/face recognition."""
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    confidence = Column(Float, nullable=False)
    image_path = Column(String(255), nullable=True)

    customer = relationship("Customer", back_populates="visits")


class Review(Base):
    """Log of customer product/store reviews and sentiment analysis predictions."""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    review_text = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=False)  # Positive, Neutral, Negative
    confidence = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    customer = relationship("Customer", back_populates="reviews")


class ChatLog(Base):
    """Log of customer interactions with retail FAQ Chatbot."""
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    intent = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class PredictionLog(Base):
    """Audit log of all AI model inference requests."""
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    prediction_type = Column(String(50), nullable=False, index=True)  # Product, Face, Sentiment, Chatbot
    input_summary = Column(Text, nullable=False)
    predicted_label = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
