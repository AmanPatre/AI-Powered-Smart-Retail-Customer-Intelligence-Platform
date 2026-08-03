"""Retail FAQ Chatbot Service using Hybrid Rule-Based + TF-IDF Machine Learning Intent Classifier."""

import json
import random
import re
from typing import Dict, List, Tuple, Any
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from app.core.config import settings
from app.core.logging import logger


class ChatbotService:
    """Hybrid intent classifier combining regex pattern matching with ML fallback."""

    def __init__(self, intents_path: Path = settings.INTENTS_FILE):
        self.intents_path = intents_path
        self.intents_data: List[Dict[str, Any]] = []
        self.intent_map: Dict[str, Dict[str, Any]] = {}
        self.pipeline: Pipeline = None
        self._load_intents_and_train_classifier()

    def _load_intents_and_train_classifier(self) -> None:
        """Load intents from JSON file and train TF-IDF ML intent classifier."""
        if not self.intents_path.exists():
            logger.error(f"Intents file not found at {self.intents_path}")
            return

        with open(self.intents_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.intents_data = data.get("intents", [])

        patterns = []
        labels = []

        for intent in self.intents_data:
            tag = intent["tag"]
            self.intent_map[tag] = intent
            for pattern in intent["patterns"]:
                patterns.append(pattern.lower())
                labels.append(tag)

        # Train TF-IDF classifier for intents
        if patterns:
            self.pipeline = Pipeline([
                ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
                ("clf", LogisticRegression(C=2.0, max_iter=200, random_state=42))
            ])
            self.pipeline.fit(patterns, labels)
            logger.info("Chatbot TF-IDF intent classifier trained successfully.")

    def _match_rule_based(self, text: str) -> Tuple[str, float]:
        """Check direct pattern regex matches for deterministic responses."""
        clean_input = text.lower().strip()

        for intent in self.intents_data:
            tag = intent["tag"]
            for pattern in intent["patterns"]:
                p_clean = pattern.lower().strip()
                # Exact match or word boundary regex match
                if p_clean in clean_input or clean_input in p_clean:
                    return tag, 0.95
                if re.search(r"\b" + re.escape(p_clean) + r"\b", clean_input):
                    return tag, 0.98

        return None, 0.0

    def get_response(self, text: str) -> Tuple[str, str, float]:
        """Process user text message and return (bot_response, intent_tag, confidence)."""
        if not text or not text.strip():
            return "I didn't quite receive your message. Could you please repeat your question?", "unknown", 0.0

        # Step 1: Rule-based check
        tag, confidence = self._match_rule_based(text)

        # Step 2: Machine Learning classifier fallback
        if not tag and self.pipeline:
            clean_input = text.lower().strip()
            probs = self.pipeline.predict_proba([clean_input])[0]
            classes = self.pipeline.classes_
            max_idx = probs.argmax()
            max_prob = probs[max_idx]

            if max_prob >= 0.25:  # Threshold for intent match
                tag = str(classes[max_idx])
                confidence = float(max_prob)

        # Step 3: Default fallback if unmapped
        if not tag or tag not in self.intent_map:
            tag = "fallback"
            confidence = 0.0
            response = "I'm sorry, I couldn't quite understand that. You can ask me about store hours, locations, return policies, order tracking, or payment methods!"
            return response, tag, confidence

        # Pick random response from matched intent
        intent_info = self.intent_map[tag]
        responses = intent_info.get("responses", [])
        bot_response = random.choice(responses) if responses else "How can I assist you with your retail shopping today?"

        return bot_response, tag, round(confidence, 4)


# Singleton instance
chatbot_service = ChatbotService()
