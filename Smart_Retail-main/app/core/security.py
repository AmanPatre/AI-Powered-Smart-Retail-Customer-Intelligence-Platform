"""Security and API Key authentication dependencies."""

from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.core.config import settings
from app.core.logging import logger

api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Verify that incoming request header contains valid API key.
    
    Permits access if API key matches setting or during debug testing when header is passed.
    """
    if not api_key:
        logger.warning("API Key missing in request headers.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key header 'X-API-Key'.",
        )
    if api_key != settings.API_KEY:
        logger.warning(f"Invalid API Key provided: {api_key[:4]}***")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key provided.",
        )
    return api_key
