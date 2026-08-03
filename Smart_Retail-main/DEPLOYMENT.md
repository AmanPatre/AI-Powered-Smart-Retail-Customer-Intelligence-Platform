# 🚀 Production Deployment Guide (Render & Docker)

This guide details how to deploy the **Smart Retail Platform** locally using Docker Compose and in production cloud environments such as **Render**.

---

## Option 1: Docker Local / VPS Deployment

### 1. Build and Launch Containers
Ensure Docker and Docker Compose are installed on your server, then execute:

```bash
docker compose up --build -d
```

### 2. Verify Container Health
```bash
docker compose ps
```

FastAPI server runs on port `8000`, and Streamlit dashboard runs on port `8501`.

---

## Option 2: Deploying to Render.com

Render supports single-command Docker deployments and web services.

### Deploying FastAPI Web Service on Render:
1. Connect your repository to Render.
2. Select **Web Service** -> **Docker Runtime**.
3. Environment Variables to add on Render Dashboard:
   - `API_KEY`: `your_secure_random_api_key`
   - `DATABASE_URL`: `sqlite:////app/data/smart_retail.db`
   - `PORT`: `8000`
4. Set Docker Build Context to `./` and Dockerfile to `./Dockerfile`.

### Deploying Streamlit Dashboard on Render:
1. Create a second **Web Service** on Render.
2. Environment Variables:
   - `API_BASE_URL`: `https://your-fastapi-service.onrender.com`
   - `API_KEY`: `your_secure_random_api_key`
3. Set Start Command to:
   ```bash
   streamlit run dashboard/app.py --server.port=10000 --server.address=0.0.0.0
   ```
