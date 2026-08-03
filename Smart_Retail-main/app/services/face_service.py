"""Face Recognition Service using OpenCV and facial feature encodings."""

import io
import json
import numpy as np
from typing import Tuple, Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.core.logging import logger
from app.models.db_models import Customer, Visit

try:
    import cv2
    HAS_OPENCV = hasattr(cv2, "CascadeClassifier")
except ImportError:
    cv2 = None
    HAS_OPENCV = False

try:
    import face_recognition
    HAS_FACE_RECOGNITION = True
except ImportError:
    HAS_FACE_RECOGNITION = False
    logger.info("face_recognition (dlib) package not found. Using OpenCV HOG/Histogram 128-d feature extractor fallback.")


class FaceService:
    """Service for face detection, encoding generation, customer recognition, and visit logging."""

    def __init__(self):
        # Load OpenCV Haar Cascade face detector if available
        if HAS_OPENCV and hasattr(cv2, "data") and hasattr(cv2.data, "haarcascades"):
            try:
                self.cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
                self.face_cascade = cv2.CascadeClassifier(self.cascade_path)
            except Exception as e:
                logger.warning(f"Failed to load OpenCV CascadeClassifier: {e}")
                self.face_cascade = None
        else:
            self.cascade_path = None
            self.face_cascade = None

    def decode_image(self, image_bytes: bytes) -> np.ndarray:
        """Decode raw image byte stream to OpenCV BGR numpy array."""
        if HAS_OPENCV and hasattr(cv2, "imdecode"):
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is not None:
                return img
        # Fallback using PIL
        from PIL import Image
        pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return np.array(pil_img)[:, :, ::-1]  # RGB to BGR

    def detect_faces_opencv(self, img_bgr: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces in BGR image using OpenCV Haar Cascades."""
        if not self.face_cascade or not HAS_OPENCV:
            h, w = img_bgr.shape[:2]
            return [(0, 0, w, h)]
        try:
            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )
            return [(int(x), int(y), int(w), int(h)) for (x, y, w, h) in faces]
        except Exception as e:
            logger.warning(f"OpenCV face detection error: {e}")
            h, w = img_bgr.shape[:2]
            return [(0, 0, w, h)]

    def extract_encoding(self, img_bgr: np.ndarray, face_rect: Optional[Tuple[int, int, int, int]] = None) -> List[float]:
        """Generate normalized 128-dimensional feature encoding vector for face."""
        if HAS_FACE_RECOGNITION and HAS_OPENCV and hasattr(cv2, "cvtColor"):
            rgb_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_img)
            if encodings:
                return encodings[0].tolist()

        # OpenCV / NumPy Fallback Feature Extractor (128-d vector)
        if face_rect:
            x, y, w, h = face_rect
            face_chip = img_bgr[y:y+h, x:x+w]
        else:
            face_chip = img_bgr

        if HAS_OPENCV and hasattr(cv2, "cvtColor") and hasattr(cv2, "calcHist"):
            gray_chip = cv2.cvtColor(face_chip, cv2.COLOR_BGR2GRAY)
            hist = cv2.calcHist([gray_chip], [0], None, [128], [0, 256]).flatten()
        else:
            gray_chip = np.mean(face_chip, axis=2).astype(np.uint8)
            hist, _ = np.histogram(gray_chip, bins=128, range=(0, 256))
            hist = hist.astype(np.float32)

        norm_factor = np.linalg.norm(hist)
        if norm_factor > 0:
            hist = hist / norm_factor
        return hist.tolist()

    def find_matching_customer(
        self, target_encoding: List[float], db: Session, tolerance: float = 0.6
    ) -> Tuple[Optional[Customer], float]:
        """Search database customers for nearest matching face encoding based on L2 Euclidean distance."""
        customers = db.query(Customer).all()
        if not customers:
            return None, 0.0

        target_vec = np.array(target_encoding)
        best_match = None
        min_distance = float("inf")

        for customer in customers:
            try:
                db_vec = np.array(customer.get_face_encoding())
                if len(db_vec) != len(target_vec):
                    continue
                dist = np.linalg.norm(db_vec - target_vec)
                if dist < min_distance:
                    min_distance = dist
                    best_match = customer
            except Exception as e:
                logger.error(f"Error comparing customer {customer.id}: {e}")
                continue

        # Convert Euclidean distance to confidence score (1.0 = perfect match)
        if min_distance <= tolerance and best_match:
            confidence = max(0.0, min(1.0, 1.0 - (min_distance / tolerance)))
            return best_match, round(confidence, 4)

        return None, 0.0

    def process_face_recognition(
        self, image_bytes: bytes, db: Session
    ) -> Dict[str, Any]:
        """Process face detection, customer recognition, and visit log creation."""
        img_bgr = self.decode_image(image_bytes)
        face_rects = self.detect_faces_opencv(img_bgr)
        faces_count = len(face_rects)

        if faces_count == 0:
            return {
                "recognized": False,
                "customer": None,
                "confidence": 0.0,
                "visit_id": None,
                "faces_detected": 0,
                "message": "No face detected in uploaded image.",
            }

        # Generate encoding for primary face
        primary_face = face_rects[0]
        encoding = self.extract_encoding(img_bgr, primary_face)

        # Match against customer database
        matched_customer, confidence = self.find_matching_customer(encoding, db)

        visit_id = None
        if matched_customer:
            # Record visit in database
            new_visit = Visit(
                customer_id=matched_customer.id,
                confidence=confidence,
                image_path=None
            )
            db.add(new_visit)
            db.commit()
            db.refresh(new_visit)
            visit_id = new_visit.id
            message = f"Welcome back, {matched_customer.name}!"
        else:
            message = "Face detected, but customer is not registered in the system."

        return {
            "recognized": bool(matched_customer is not None),
            "customer": matched_customer,
            "confidence": confidence,
            "visit_id": visit_id,
            "faces_detected": faces_count,
            "message": message,
        }


# Singleton instance
face_service = FaceService()
