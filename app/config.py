"""Configuration management for the application"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    embedding_model: str = "text-embedding-3-small"

    # Application Configuration
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k_results: int = 3
    confidence_threshold: float = 0.5

    # Database Configuration
    chroma_db_path: str = "./data/chroma_db"
    chroma_collection_name: str = "documents"

    # Server Configuration
    debug: bool = True
    log_level: str = "INFO"
    max_upload_size_mb: int = 10

    # CORS Configuration
    allowed_origins: list = ["*"]

    class Config:
        """Pydantic config"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create global settings instance
settings = Settings()
