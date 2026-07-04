"""Tests for embedding service"""

import pytest
from app.services.embedding_service import EmbeddingService
from app.utils.errors import EmbeddingError
from unittest.mock import patch, MagicMock


class TestEmbeddingService:
    """Test embedding service functionality"""

    @pytest.fixture
    def service(self):
        """Create embedding service instance"""
        return EmbeddingService()

    @patch('openai.Embedding.create')
    def test_generate_embedding(self, mock_create, service):
        """Test embedding generation"""
        # Mock the API response
        mock_create.return_value = {
            "data": [{"embedding": [0.1, 0.2, 0.3] * 512}]  # 1536 dims
        }
        
        embedding = service.generate_embedding("test text")
        
        assert isinstance(embedding, list)
        assert len(embedding) > 0

    @patch('openai.Embedding.create')
    def test_embedding_cache(self, mock_create, service):
        """Test that embeddings are cached"""
        mock_create.return_value = {
            "data": [{"embedding": [0.1, 0.2, 0.3] * 512}]
        }
        
        text = "test text"
        embedding1 = service.generate_embedding(text)
        embedding2 = service.generate_embedding(text)
        
        # Should only call API once due to cache
        assert mock_create.call_count == 1
        assert embedding1 == embedding2

    def test_clear_cache(self, service):
        """Test cache clearing"""
        # Add something to cache
        service.cache["test"] = MagicMock()
        assert len(service.cache) > 0
        
        # Clear cache
        service.clear_cache()
        assert len(service.cache) == 0

    @patch('openai.Embedding.create')
    def test_generate_embeddings_batch(self, mock_create, service):
        """Test batch embedding generation"""
        mock_create.return_value = {
            "data": [{"embedding": [0.1, 0.2, 0.3] * 512}]
        }
        
        texts = ["text1", "text2", "text3"]
        embeddings = service.generate_embeddings(texts)
        
        assert len(embeddings) == 3
