"""Dashboard Statistics Analytics API Route."""

from collections import Counter
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_api_key
from app.schemas.dashboard import DashboardStatsResponse
from app.models.db_models import Customer, Visit, Review, ChatLog
from app.core.logging import logger

router = APIRouter(tags=["Dashboard & Analytics"])


@router.get(
    "/dashboard/stats",
    response_model=DashboardStatsResponse,
    dependencies=[Depends(verify_api_key)],
)
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Retrieve consolidated analytics metrics for dashboard visualization."""
    try:
        total_customers = db.query(Customer).count()
        total_visits = db.query(Visit).count()
        total_reviews = db.query(Review).count()
        total_chat_queries = db.query(ChatLog).count()

        # Sentiment breakdown calculation
        reviews = db.query(Review).all()
        sentiment_counts = Counter([r.sentiment for r in reviews])
        sentiment_breakdown = {
            "Positive": sentiment_counts.get("Positive", 0),
            "Neutral": sentiment_counts.get("Neutral", 0),
            "Negative": sentiment_counts.get("Negative", 0),
        }

        # Top chatbot intents calculation
        chats = db.query(ChatLog).all()
        intent_counts = Counter([c.intent for c in chats])
        top_intents = dict(intent_counts.most_common(5))

        # Recent 5 visits
        recent_visit_objs = (
            db.query(Visit).order_by(Visit.timestamp.desc()).limit(5).all()
        )
        recent_visits = [
            {
                "visit_id": v.id,
                "customer_name": v.customer.name if v.customer else "Unknown",
                "timestamp": v.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "confidence": round(v.confidence, 2),
            }
            for v in recent_visit_objs
        ]

        # Recent 5 reviews
        recent_review_objs = (
            db.query(Review).order_by(Review.timestamp.desc()).limit(5).all()
        )
        recent_reviews = [
            {
                "review_id": r.id,
                "customer_name": r.customer.name if r.customer else "Anonymous",
                "review_text": r.review_text,
                "sentiment": r.sentiment,
                "confidence": round(r.confidence, 2),
                "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for r in recent_review_objs
        ]

        return DashboardStatsResponse(
            total_customers=total_customers,
            total_visits=total_visits,
            total_reviews=total_reviews,
            total_chat_queries=total_chat_queries,
            sentiment_breakdown=sentiment_breakdown,
            top_intents=top_intents,
            recent_visits=recent_visits,
            recent_reviews=recent_reviews,
            system_status="Operational",
        )
    except Exception as e:
        logger.error(f"Dashboard stats endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching dashboard statistics: {str(e)}",
        )
