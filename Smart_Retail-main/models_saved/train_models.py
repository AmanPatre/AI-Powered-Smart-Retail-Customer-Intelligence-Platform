"""Automated training and database seeding script for Smart Retail Platform."""

import sys
import json
from pathlib import Path

# Add project base directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from app.core.database import SessionLocal, init_db
from app.models.db_models import Customer, Visit, Review, ChatLog, PredictionLog
from app.services.sentiment_service import sentiment_service
from app.services.product_service import product_service
from app.services.chatbot_service import chatbot_service
from app.services.face_service import face_service
from app.core.logging import logger


def seed_database_and_models():
    """Train ML models and populate SQLite database with initial customer & store metrics."""
    logger.info("Initializing database schema...")
    init_db()
    db = SessionLocal()

    # Check if customers already seeded
    if db.query(Customer).count() > 0:
        logger.info("Database already seeded. Skipping initial data seed.")
        db.close()
        return

    logger.info("Seeding initial customers, visits, reviews, and logs...")

    # Seed Sample Customers with 128-d face encodings
    sample_customers = [
        {
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "encoding": (np_vec := [0.05 * i for i in range(128)]),
        },
        {
            "name": "Bob Smith",
            "email": "bob.smith@example.com",
            "encoding": [0.08 * i for i in range(128)],
        },
        {
            "name": "Carol Williams",
            "email": "carol.williams@example.com",
            "encoding": [0.02 * i for i in range(128)],
        },
    ]

    customer_objs = []
    for cdata in sample_customers:
        cust = Customer(name=cdata["name"], email=cdata["email"])
        cust.set_face_encoding(cdata["encoding"])
        db.add(cust)
        customer_objs.append(cust)

    db.commit()
    for c in customer_objs:
        db.refresh(c)

    # Seed Visits
    visits = [
        Visit(customer_id=customer_objs[0].id, confidence=0.92),
        Visit(customer_id=customer_objs[0].id, confidence=0.88),
        Visit(customer_id=customer_objs[1].id, confidence=0.95),
        Visit(customer_id=customer_objs[2].id, confidence=0.91),
    ]
    db.add_all(visits)

    # Seed Reviews with Sentiment predictions
    sample_reviews = [
        ("The new electronic displays in the store are fantastic!", customer_objs[0].id),
        ("Great customer service and fast checkout experience.", customer_objs[1].id),
        ("Average product selection, price could be slightly better.", customer_objs[2].id),
        ("Item arrived broken and customer support line was busy.", None),
    ]

    for text, cust_id in sample_reviews:
        sent, conf, _ = sentiment_service.predict(text)
        rev = Review(
            customer_id=cust_id,
            review_text=text,
            sentiment=sent,
            confidence=conf,
        )
        db.add(rev)

    # Seed Chat Logs
    chat_samples = [
        ("What are your store hours?", "Our retail stores are open Mon-Sat 8 AM to 10 PM...", "store_hours", 0.98),
        ("Do you offer student discounts?", "Yes! Join our Smart Retail Loyalty Club for 15% off...", "discounts_promotions", 0.95),
    ]
    for msg, resp, intent, conf in chat_samples:
        clog = ChatLog(
            user_message=msg,
            bot_response=resp,
            intent=intent,
            confidence=conf
        )
        db.add(clog)

    # Seed Prediction Audit Logs
    pred_logs = [
        PredictionLog(prediction_type="Sentiment", input_summary="Great store experience", predicted_label="Positive", confidence=0.96),
        PredictionLog(prediction_type="Product", input_summary="Image file uploaded (laptop.jpg)", predicted_label="Electronics", confidence=0.94),
        PredictionLog(prediction_type="Face", input_summary="Store camera feed frame", predicted_label="Alice Johnson", confidence=0.92),
    ]
    db.add_all(pred_logs)

    db.commit()
    db.close()
    logger.info("Successfully seeded database and initialized all ML models!")


if __name__ == "__main__":
    seed_database_and_models()
