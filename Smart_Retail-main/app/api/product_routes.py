"""Product Image Classification API Route."""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_api_key
from app.schemas.product import ProductClassificationResponse
from app.services.product_service import product_service
from app.models.db_models import PredictionLog
from app.core.logging import logger

router = APIRouter(tags=["Product Classification"])


@router.post(
    "/classify-product",
    response_model=ProductClassificationResponse,
    dependencies=[Depends(verify_api_key)],
)
async def classify_product(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Classify retail product category from an uploaded product image using MobileNetV2."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File provided must be a valid image format (JPEG, PNG).",
        )

    try:
        image_bytes = await file.read()
        category, confidence, prob_dict = product_service.classify_product(image_bytes)

        # Audit log prediction
        pred_log = PredictionLog(
            prediction_type="Product Classification",
            input_summary=f"Filename: {file.filename}, Size: {len(image_bytes)} bytes",
            predicted_label=category,
            confidence=confidence,
        )
        db.add(pred_log)
        db.commit()

        return ProductClassificationResponse(
            category=category,
            confidence=confidence,
            probabilities=prob_dict,
            message="Product image classified successfully.",
        )
    except Exception as e:
        logger.error(f"Product classification endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during product classification: {str(e)}",
        )
