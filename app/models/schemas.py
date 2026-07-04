"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChunkMetadata(BaseModel):
    """Metadata for a document chunk"""
    page_number: int
    chunk_index: int
    source_length: int


class SourceReference(BaseModel):
    """Reference to a source chunk"""
    page_number: int
    chunk_index: int
    text_preview: str
    relevance_score: float = Field(..., ge=0, le=1)


class DocumentUploadResponse(BaseModel):
    """Response after document upload"""
    document_id: str
    filename: str
    total_chunks: int
    extracted_text_length: int
    processing_time_seconds: float
    message: str = "Document processed successfully"


class QueryRequest(BaseModel):
    """Request for asking a question"""
    question: str = Field(..., min_length=1, max_length=1000)
    document_id: str


class QueryResponse(BaseModel):
    """Response to a question"""
    answer: str
    confidence_score: float = Field(..., ge=0, le=1)
    sources: List[SourceReference]
    processing_time_seconds: float
    is_confident: bool  # True if answer found, False for "I don't know"


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    services: dict = {}
