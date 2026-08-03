"""FastAPI Application Main Entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import init_db
from app.core.logging import logger
from app.api.router import api_router
from models_saved.train_models import seed_database_and_models

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-Ready AI-Powered Smart Retail & Customer Intelligence Platform API",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Event handler for FastAPI startup: Initializes database and seeds default models."""
    logger.info("Initializing Smart Retail Platform API background services...")
    init_db()
    seed_database_and_models()
    logger.info("Application startup complete. API is ready to process requests.")


@app.get("/", tags=["Root"])
async def root():
    """Root landing endpoint with system navigation info."""
    return JSONResponse(
        content={
            "platform": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "documentation": "/docs",
            "health_check": "/health",
            "status": "Operational",
        }
    )


# Include main API router
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
