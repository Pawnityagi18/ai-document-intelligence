"""Health check routes"""

from fastapi import APIRouter
from app.models.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        services={
            "document_processor": "ok",
            "embedding_service": "ok",
            "vector_store": "ok",
            "llm_service": "ok"
        }
    )
