"""Main FastAPI application"""

import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from app.logging_config import setup_logging
from app.routes import health, documents, queries

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Document Intelligence",
    description="Upload documents and ask questions with RAG",
    version="0.1.0"
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(documents.router)
app.include_router(queries.router)

# Mount static files (frontend)
frontend_dir = Path("frontend")
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
    logger.info("Frontend static files mounted")
else:
    logger.warning("Frontend directory not found")


@app.get("/")
async def serve_index() -> FileResponse:
    """Serve the main frontend HTML"""
    index_path = Path("frontend/index.html")
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "AI Document Intelligence API"}


@app.on_event("startup")
async def startup_event():
    """Called when application starts"""
    logger.info("Application starting up...")
    logger.info(f"OpenAI Model: {settings.openai_model}")
    logger.info(f"Embedding Model: {settings.embedding_model}")
    logger.info(f"Chunk Size: {settings.chunk_size}")
    logger.info(f"Confidence Threshold: {settings.confidence_threshold}")


@app.on_event("shutdown")
async def shutdown_event():
    """Called when application shuts down"""
    logger.info("Application shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level.lower()
    )
