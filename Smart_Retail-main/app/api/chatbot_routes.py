"""Retail FAQ Chatbot API Route."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_api_key
from app.schemas.chatbot import ChatRequest, ChatResponse
from app.services.chatbot_service import chatbot_service
from app.models.db_models import ChatLog, PredictionLog
from app.core.logging import logger

router = APIRouter(tags=["Retail Chatbot"])


@router.post(
    "/chatbot",
    response_model=ChatResponse,
    dependencies=[Depends(verify_api_key)],
)
async def chatbot_query(
    payload: ChatRequest,
    db: Session = Depends(get_db),
):
    """Answer customer retail questions using hybrid rule-based + ML intent classifier."""
    try:
        response_text, intent, confidence = chatbot_service.get_response(payload.message)

        # Log conversation in ChatLog table
        chat_log = ChatLog(
            user_message=payload.message,
            bot_response=response_text,
            intent=intent,
            confidence=confidence,
        )
        db.add(chat_log)
        db.commit()
        db.refresh(chat_log)

        # Log prediction audit entry
        pred_log = PredictionLog(
            prediction_type="Chatbot Intent",
            input_summary=payload.message[:100],
            predicted_label=intent,
            confidence=confidence,
        )
        db.add(pred_log)
        db.commit()

        return ChatResponse(
            response=response_text,
            intent=intent,
            confidence=confidence,
            log_id=chat_log.id,
        )
    except Exception as e:
        logger.error(f"Chatbot query endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while generating chatbot response: {str(e)}",
        )
