"""Sentiment Analysis API Route."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_api_key
from app.schemas.sentiment import SentimentRequest, SentimentResponse
from app.services.sentiment_service import sentiment_service
from app.models.db_models import Review, PredictionLog
from app.core.logging import logger

router = APIRouter(tags=["Sentiment Analysis"])


@router.post(
    "/analyze-sentiment",
    response_model=SentimentResponse,
    dependencies=[Depends(verify_api_key)],
)
async def analyze_sentiment(
    payload: SentimentRequest,
    db: Session = Depends(get_db),
):
    """Analyze customer review text and return sentiment prediction (Positive, Neutral, Negative)."""
    try:
        cleaned_text = sentiment_service.clean_text(payload.review_text)
        sentiment, confidence, probs = sentiment_service.predict(payload.review_text)

        # Save to Review database table
        new_review = Review(
            customer_id=payload.customer_id,
            review_text=payload.review_text,
            sentiment=sentiment,
            confidence=confidence,
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)

        # Log prediction audit entry
        pred_log = PredictionLog(
            prediction_type="Sentiment Analysis",
            input_summary=payload.review_text[:100],
            predicted_label=sentiment,
            confidence=confidence,
        )
        db.add(pred_log)
        db.commit()

        return SentimentResponse(
            sentiment=sentiment,
            confidence=confidence,
            probabilities=probs,
            cleaned_text=cleaned_text,
            review_id=new_review.id,
        )
    except Exception as e:
        logger.error(f"Sentiment analysis endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during sentiment analysis: {str(e)}",
        )
