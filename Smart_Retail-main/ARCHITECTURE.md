# 🏗️ Architecture & System Design Document

## Overview

The **Smart Retail & Customer Intelligence Platform** is structured following Clean Architecture and SOLID design principles. It decouples machine learning inference engines, data persistence, REST API presentation, and dashboard visualization.

---

## 📐 High-Level Architecture Diagram

```
+-----------------------------------------------------------------------+
|                            USER INTERFACES                            |
|  +----------------------------+        +---------------------------+  |
|  |   Streamlit Web Dashboard  |        |    External API Client    |  |
|  |     (Port 8501 / UI)       |        |     (REST / Swagger)      |  |
|  +--------------+-------------+        +-------------+-------------+  |
+-----------------|------------------------------------|----------------+
                  | HTTP Requests (X-API-Key)          |
                  v                                    v
+-----------------------------------------------------------------------+
|                           FASTAPI BACKEND                             |
|  +-----------------------------------------------------------------+  |
|  |                        Security Header                          |  |
|  |                    (X-API-Key Verification)                     |  |
|  +--------------------------------+--------------------------------+  |
|                                   |                                   |
|  +--------------------------------v--------------------------------+  |
|  |                         API ROUTERS                             |  |
|  |   /recognize-face | /classify-product | /analyze-sentiment |    |  |
|  |               /chatbot | /dashboard/stats | /health             |  |
|  +--------------------------------+--------------------------------+  |
+-----------------------------------|-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                          MACHINE LEARNING SERVICES                    |
|  +---------------+  +------------------+  +---------------+  +------+  |
|  |  FaceService  |  |  ProductService  |  |SentimentServ. |  |Chat. |  |
|  | (OpenCV / L2) |  | (MobileNetV2 H5) |  | (TFIDF + LR)  |  | (ML) |  |
|  +-------+-------+  +--------+---------+  +-------+-------+  +---+--+  |
+----------|-------------------|--------------------|--------------|----+
           |                   |                    |              |
           +-------------------+---------+----------+--------------+
                                         |
                                         v
+-----------------------------------------------------------------------+
|                          PERSISTENCE LAYER                            |
|  +-----------------------------------------------------------------+  |
|  |                     SQLAlchemy ORM + SQLite                     |  |
|  |   [Customers]  [Visits]  [Reviews]  [ChatLogs]  [PredLogs]      |  |
|  +-----------------------------------------------------------------+  |
+-----------------------------------------------------------------------+
```

---

## 🔑 Design Principles

1. **Single Responsibility Principle (SRP):** Each service (`face_service`, `product_service`, `sentiment_service`, `chatbot_service`) manages its own independent ML pipeline and preprocessing rules.
2. **Dependency Injection:** Database sessions (`SessionLocal`) and security checks are injected into FastAPI routes using `Depends()`.
3. **Resilience & Fallbacks:** Image classification and face detection engines include fallback mechanisms so the application remains 100% operational across hardware environments.
4. **Audit Logging:** Every AI model prediction is stored in `prediction_logs` for compliance and model performance tracking.
