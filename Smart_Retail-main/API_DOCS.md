# 📖 API Endpoint Documentation & Examples

All API requests require the security header `X-API-Key`.

Base URL: `http://localhost:8000`

---

## Endpoints Summary

| Method | Endpoint | Description | Security |
|--------|----------|-------------|----------|
| GET | `/health` | API & ML readiness status | Public |
| POST | `/recognize-face` | Face detection & returning customer match | `X-API-Key` |
| POST | `/classify-product` | MobileNetV2 product category classifier | `X-API-Key` |
| POST | `/analyze-sentiment` | TF-IDF + Logistic Regression sentiment prediction | `X-API-Key` |
| POST | `/chatbot` | Retail FAQ Chatbot intent answer | `X-API-Key` |
| GET | `/dashboard/stats` | Consolidated store analytics & metrics | `X-API-Key` |

---

## 1. Recognize Face (`POST /recognize-face`)

**Header:**
```http
X-API-Key: smart_retail_secret_key_2026
```

**Body (Multipart Form):**
- `file`: Image file (JPEG/PNG)

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/recognize-face" \
  -H "X-API-Key: smart_retail_secret_key_2026" \
  -F "file=@customer.jpg"
```

**Sample Response:**
```json
{
  "recognized": true,
  "customer": {
    "name": "Alice Johnson",
    "email": "alice.johnson@example.com",
    "id": 1,
    "created_at": "2026-08-03T11:00:00"
  },
  "confidence": 0.92,
  "visit_id": 5,
  "faces_detected": 1,
  "message": "Welcome back, Alice Johnson!"
}
```

---

## 2. Classify Product (`POST /classify-product`)

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/classify-product" \
  -H "X-API-Key: smart_retail_secret_key_2026" \
  -F "file=@laptop.jpg"
```

**Sample Response:**
```json
{
  "category": "Electronics",
  "confidence": 0.965,
  "probabilities": {
    "Apparel": 0.01,
    "Electronics": 0.965,
    "Footwear": 0.005,
    "Groceries": 0.01,
    "Home Goods": 0.01
  },
  "message": "Product image classified successfully."
}
```

---

## 3. Analyze Sentiment (`POST /analyze-sentiment`)

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/analyze-sentiment" \
  -H "X-API-Key: smart_retail_secret_key_2026" \
  -H "Content-Type: application/json" \
  -d '{"review_text": "The store environment is amazing and cashiers are super fast!"}'
```

**Sample Response:**
```json
{
  "sentiment": "Positive",
  "confidence": 0.9542,
  "probabilities": {
    "Positive": 0.9542,
    "Neutral": 0.0311,
    "Negative": 0.0147
  },
  "cleaned_text": "the store environment is amazing and cashiers are super fast",
  "review_id": 12
}
```

---

## 4. Retail Chatbot (`POST /chatbot`)

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/chatbot" \
  -H "X-API-Key: smart_retail_secret_key_2026" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your store hours on Sunday?"}'
```

**Sample Response:**
```json
{
  "response": "Our retail stores are open daily! Mon-Sat: 8 AM - 10 PM, Sun: 9 AM - 8 PM.",
  "intent": "store_hours",
  "confidence": 0.98,
  "log_id": 8
}
```

---

## 5. Dashboard Stats (`GET /dashboard/stats`)

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/dashboard/stats" \
  -H "X-API-Key: smart_retail_secret_key_2026"
```
