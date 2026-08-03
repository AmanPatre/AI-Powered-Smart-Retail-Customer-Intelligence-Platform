"""Pytest configuration and shared test fixtures."""

import os
import io
import cv2
import numpy as np
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.config import settings
from app.core.database import Base, get_db
from models_saved.train_models import seed_database_and_models

# Use an in-memory SQLite database for fast unit testing
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create test database schema and seed initial model data."""
    Base.metadata.create_all(bind=engine)
    
    # Override get_db dependency
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    
    # Seed database models
    seed_database_and_models()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """FastAPI TestClient instance."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers():
    """Valid API Key security headers."""
    return {settings.API_KEY_NAME: settings.API_KEY}


@pytest.fixture
def sample_image_bytes():
    """Generate synthetic RGB test image in JPEG byte format containing a face-like structure."""
    img = np.zeros((224, 224, 3), dtype=np.uint8)
    # Draw simple circle representing face for OpenCV cascade detector
    cv2.circle(img, (112, 112), 60, (200, 200, 200), -1)
    cv2.circle(img, (90, 90), 10, (50, 50, 50), -1)   # Left eye
    cv2.circle(img, (134, 90), 10, (50, 50, 50), -1)  # Right eye
    cv2.ellipse(img, (112, 135), (25, 10), 0, 0, 180, (50, 50, 50), 3)  # Mouth

    is_success, buffer = cv2.imencode(".jpg", img)
    return io.BytesIO(buffer.tobytes())
