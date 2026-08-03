"""Face Recognition API Route."""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_api_key
from app.schemas.face import FaceRecognitionResponse
from app.services.face_service import face_service
from app.models.db_models import PredictionLog
from app.core.logging import logger

router = APIRouter(tags=["Face Recognition"])


@router.post(
    "/recognize-face",
    response_model=FaceRecognitionResponse,
    dependencies=[Depends(verify_api_key)],
)
async def recognize_face(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Detect face in uploaded image, recognize returning customer, and log visit."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File provided must be a valid image format (JPEG, PNG).",
        )

    try:
        image_bytes = await file.read()
        result = face_service.process_face_recognition(image_bytes, db)

        # Audit log prediction
        customer_name = result["customer"].name if result["customer"] else "Unrecognized Face"
        pred_log = PredictionLog(
            prediction_type="Face Recognition",
            input_summary=f"Filename: {file.filename}, Size: {len(image_bytes)} bytes",
            predicted_label=customer_name,
            confidence=result["confidence"],
        )
        db.add(pred_log)
        db.commit()

        return result
    except Exception as e:
        logger.error(f"Face recognition endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing face recognition: {str(e)}",
        )
