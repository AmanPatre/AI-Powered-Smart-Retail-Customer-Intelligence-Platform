# AI-Powered Smart Retail & Customer Intelligence Platform

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

A production-grade, modular, end-to-end **Smart Retail Analytics & Customer Intelligence Engine** built entirely in Python. It integrates Deep Learning Computer Vision (MobileNetV2, OpenCV), Natural Language Processing (TF-IDF, Logistic Regression), SQL persistence, security, automated testing, and a real-time Streamlit visualization dashboard.

---

## Key Features

1. **Product Image Classification (MobileNetV2)**
   - Transfer learning using Keras MobileNetV2.
   - Categorizes retail products into `Apparel`, `Electronics`, `Footwear`, `Groceries`, and `Home Goods`.
   - Returns top prediction, confidence score, and full probability map.

2. **Returning Customer Face Recognition (OpenCV)**
   - Detects faces in camera frames using OpenCV cascades.
   - Extracts 128-dimensional facial feature vectors.
   - Identifies returning customers via L2 Euclidean distance matching.
   - Automatically logs customer visit timestamps in SQLite.

3. **Customer Review Sentiment Analysis (NLP)**
   - Preprocesses raw customer text (regex cleaning, lowercasing, stop-words).
   - Machine Learning TF-IDF Vectorizer + Logistic Regression pipeline.
   - Classifies feedback into `Positive`, `Neutral`, or `Negative` sentiment with confidence.

4. **FAQ Retail Chatbot**
   - Hybrid intent matcher combining direct regex rules with TF-IDF ML intent classification.
   - Operates on structured retail knowledge base (`data/intents.json`).
   - Answers questions regarding store hours, locations, returns, orders, and promotions.

5. **FastAPI Production Backend**
   - Modular clean architecture with Pydantic request/response validation.
   - Header-based API key security (`X-API-Key`).
   - Interactive Swagger UI documentation at `/docs`.

6. **Streamlit Live Dashboard**
   - Consolidated KPI metric cards.
   - Real-time customer visit timelines & sentiment breakdown charts.
   - Live image upload testing for product classification & face check-in.
   - Interactive chatbot UI with intent inspection.

7. **Containerized Deployment & Pytest Suite**
   - Ready to deploy using `docker compose up`.
   - Full automated Pytest suite covering all API endpoints and security checks.

---

## Quick Start Guide

### Prerequisites
- Python 3.12 installed
- Git & Docker (Optional for containerized run)

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/your-org/smart-retail-platform.git
cd smart-retail-platform

# Create virtual environment
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Models & Database
```bash
python models_saved/train_models.py
```

### 4. Run Applications

**Start FastAPI Backend:**
```bash
uvicorn app.main:app --reload --port 8000
```
- Swagger API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

**Start Streamlit Analytics Dashboard:**
```bash
streamlit run dashboard/app.py --server.port 8501
```
- Open browser at: `http://localhost:8501`

---

## Docker Deployment

Run both the FastAPI service and Streamlit dashboard simultaneously:

```bash
docker compose up --build
```

- **FastAPI API**: `http://localhost:8000`
- **Streamlit Dashboard**: `http://localhost:8501`

---

## Running Unit Tests

Run full test suite using `pytest`:

```bash
pytest -v
```

---

## Project Structure

```
smart_retail_platform/
├── app/
│   ├── api/                  # FastAPI Endpoints (Health, Face, Product, Sentiment, Chatbot, Dashboard)
│   ├── core/                 # Config, Security, Database session, Logging
│   ├── models/               # SQLAlchemy ORM Entities (Customer, Visit, Review, ChatLog, PredictionLog)
│   ├── schemas/              # Pydantic Request/Response models
│   ├── services/             # ML inference pipelines (Face, Product, Sentiment, Chatbot)
│   └── main.py               # Application entrypoint
├── data/                     # Intents JSON & SQLite database
├── models_saved/             # Saved model artifacts & auto-train seed script
├── dashboard/                # Streamlit visualization app
├── tests/                    # Pytest test suite
├── Dockerfile & docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Security Configuration

Set your custom secret API Key in `.env`:
```env
API_KEY=smart_retail_secret_key_2026
```

Send the API Key in your request headers:
```http
X-API-Key: smart_retail_secret_key_2026
```

##AMAN PATRE##
