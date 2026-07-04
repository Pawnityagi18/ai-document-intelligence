"""Integration tests for QA service"""

import pytest
from pathlib import Path
from app.services.qa_service import QAService
from app.utils.errors import ApplicationError
from unittest.mock import patch, MagicMock


class TestQAService:
    """Test QA service end-to-end functionality"""

    @pytest.fixture
    def qa_service(self):
        """Create QA service instance"""
        return QAService()

    @pytest.fixture
    def sample_txt_file(self, tmp_path):
        """Create a sample text file for testing"""
        test_file = tmp_path / "sample.txt"
        content = """
        Python is a high-level programming language.
        It was created by Guido van Rossum in 1989.
        Python is known for its simplicity and readability.
        It supports multiple programming paradigms.
        Popular for web development, data science, and automation.
        """
        test_file.write_text(content)
        return str(test_file)

    @patch('openai.Embedding.create')
    @patch('openai.ChatCompletion.create')
    def test_process_document(self, mock_chat, mock_embed, qa_service, sample_txt_file):
        """Test document processing pipeline"""
        # Mock embedding
        mock_embed.return_value = {
            "data": [{"embedding": [0.1, 0.2, 0.3] * 512}]
        }
        
        result = qa_service.process_document(sample_txt_file, "test_doc_1")
        
        assert result["document_id"] == "test_doc_1"
        assert result["total_chunks"] > 0
        assert result["extracted_text_length"] > 0
        assert result["status"] == "success"

    @patch('openai.Embedding.create')
    @patch('openai.ChatCompletion.create')
    def test_answer_question(self, mock_chat, mock_embed, qa_service, sample_txt_file):
        """Test question answering"""
        # Mock embedding
        mock_embed.return_value = {
            "data": [{"embedding": [0.1, 0.2, 0.3] * 512}]
        }
        
        # Mock LLM response
        mock_chat.return_value = {
            "choices": [{"message": {"content": "Python is a programming language."}}]
        }
        
        # Process document first
        qa_service.process_document(sample_txt_file, "test_doc_1")
        
        # Ask question
        response = qa_service.answer_question("What is Python?", "test_doc_1")
        
        assert response.answer
        assert isinstance(response.confidence_score, float)
        assert 0 <= response.confidence_score <= 1
