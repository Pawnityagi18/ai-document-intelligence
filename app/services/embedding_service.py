"""Embedding generation service"""

import logging
from typing import List
from datetime import datetime
import openai
from app.config import settings
from app.utils.errors import EmbeddingError
from app.models.domain import EmbeddingCacheEntry

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Generate embeddings for text"""

    def __init__(self):
        """Initialize embedding service"""
        openai.api_key = settings.openai_api_key
        self.model = settings.embedding_model
        self.cache: dict[str, EmbeddingCacheEntry] = {}
        logger.info(f"Initialized EmbeddingService with model: {self.model}")

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a text string

        Args:
            text: Text to embed

        Returns:
            Embedding vector

        Raises:
            EmbeddingError: If embedding generation fails
        """
        try:
            # Check cache
            if text in self.cache:
                logger.debug(f"Cache hit for embedding")
                return self.cache[text].embedding

            logger.debug(f"Generating embedding for text length: {len(text)}")

            # Call OpenAI API
            response = openai.Embedding.create(
                input=text,
                model=self.model
            )

            embedding = response["data"][0]["embedding"]

            # Cache the embedding
            self.cache[text] = EmbeddingCacheEntry(
                text=text,
                embedding=embedding,
                created_at=datetime.now()
            )

            logger.debug(
                f"Generated embedding: dimension={len(embedding)}"
            )
            return embedding

        except Exception as e:
            error_msg = f"Failed to generate embedding: {str(e)}"
            logger.error(error_msg)
            raise EmbeddingError(error_msg) from e

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors

        Raises:
            EmbeddingError: If embedding generation fails
        """
        logger.info(f"Generating {len(texts)} embeddings")
        embeddings = []

        for i, text in enumerate(texts):
            try:
                embedding = self.generate_embedding(text)
                embeddings.append(embedding)
                if (i + 1) % 10 == 0:
                    logger.info(f"Generated {i + 1}/{len(texts)} embeddings")
            except EmbeddingError:
                logger.error(f"Failed to embed text {i}")
                raise

        logger.info(f"Successfully generated {len(embeddings)} embeddings")
        return embeddings

    def clear_cache(self) -> None:
        """Clear embedding cache"""
        cache_size = len(self.cache)
        self.cache.clear()
        logger.info(f"Cleared embedding cache ({cache_size} entries)")
