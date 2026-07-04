"""Domain models"""

from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime


@dataclass
class Chunk:
    """A chunk of document text"""
    text: str
    page_number: int
    chunk_index: int
    document_id: str
    source_length: int = 0


@dataclass
class Document:
    """A processed document"""
    document_id: str
    filename: str
    total_chunks: int
    extracted_text_length: int
    uploaded_at: datetime
    chunks: List[Chunk]


@dataclass
class QueryResult:
    """Result of a query"""
    answer: str
    confidence_score: float
    sources: List[Dict[str, Any]]
    processing_time_seconds: float
    is_confident: bool


@dataclass
class EmbeddingCacheEntry:
    """Cache entry for embeddings"""
    text: str
    embedding: List[float]
    created_at: datetime
