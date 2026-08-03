"""Sentiment Analysis Service using TF-IDF + Logistic Regression."""

import re
import joblib
import numpy as np
from typing import Tuple, Dict
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from app.core.config import settings
from app.core.logging import logger

# Seed retail reviews dataset for automatic model initialization
SEED_REVIEWS = [
    ("Great customer service, friendly staff and amazing product quality!", "Positive"),
    ("The item arrived quickly and works perfectly. Very happy with purchase.", "Positive"),
    ("Superb store environment and easy checkout process.", "Positive"),
    ("Fast shipping, excellent packaging, 5 stars!", "Positive"),
    ("Highly recommend this store, wonderful prices and discounts.", "Positive"),
    ("Awesome products and very helpful staff.", "Positive"),
    ("Love the design and quality! Will definitely shop again.", "Positive"),
    ("Item is okay, nothing special but does the job.", "Neutral"),
    ("Standard retail experience, average prices.", "Neutral"),
    ("Product is acceptable, delivery took standard time.", "Neutral"),
    ("Received product as described, no major complaints.", "Neutral"),
    ("Average store with decent variety.", "Neutral"),
    ("Poor quality item, broke on the first day of use.", "Negative"),
    ("Terrible customer service, rude cashiers and long waiting line.", "Negative"),
    ("Defective product delivered, refund process is too slow.", "Negative"),
    ("Overpriced items and horrible return policy.", "Negative"),
    ("Very disappointed with the delivery, item arrived damaged.", "Negative"),
    ("Bad experience, will never buy from this store again.", "Negative"),
]


class SentimentService:
    """Service handling text preprocessing and sentiment model classification."""

    def __init__(self, model_path: Path = settings.SENTIMENT_MODEL_PATH):
        self.model_path = model_path
        self.pipeline: Pipeline = None
        self._load_or_train_model()

    def clean_text(self, text: str) -> str:
        """Clean and normalize raw review text using regex & NLP techniques."""
        if not text:
            return ""
        # Lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
        # Remove special characters & digits
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\d+", "", text)
        # Extra whitespace reduction
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _train_default_model(self) -> Pipeline:
        """Train a TF-IDF + Logistic Regression pipeline on seed dataset."""
        logger.info("Training fresh TF-IDF + Logistic Regression Sentiment Model...")
        texts, labels = zip(*SEED_REVIEWS)
        cleaned_texts = [self.clean_text(t) for t in texts]

        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=1000)),
            ("clf", LogisticRegression(C=1.0, max_iter=200, random_state=42))
        ])

        pipeline.fit(cleaned_texts, labels)
        
        # Save model pipeline
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipeline, self.model_path)
        logger.info(f"Saved sentiment model pipeline to {self.model_path}")
        return pipeline

    def _load_or_train_model(self) -> None:
        """Load pre-trained model from disk or train a fallback default."""
        if self.model_path.exists():
            try:
                self.pipeline = joblib.load(self.model_path)
                logger.info(f"Loaded existing sentiment model from {self.model_path}")
            except Exception as e:
                logger.error(f"Failed to load sentiment model: {e}. Retraining...")
                self.pipeline = self._train_default_model()
        else:
            self.pipeline = self._train_default_model()

    def predict(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        """Predict sentiment (Positive, Neutral, Negative) and return confidence breakdown."""
        cleaned = self.clean_text(text)
        if not cleaned:
            return "Neutral", 0.5, {"Positive": 0.33, "Neutral": 0.34, "Negative": 0.33}

        probs = self.pipeline.predict_proba([cleaned])[0]
        classes = self.pipeline.classes_
        
        prob_dict = {cls: round(float(prob), 4) for cls, prob in zip(classes, probs)}
        predicted_class = str(classes[np.argmax(probs)])
        confidence = float(np.max(probs))

        return predicted_class, round(confidence, 4), prob_dict


# Singleton instance
sentiment_service = SentimentService()
