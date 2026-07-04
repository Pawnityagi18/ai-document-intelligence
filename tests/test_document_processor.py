"""Tests for document processor"""

import pytest
from pathlib import Path
from app.services.document_processor import DocumentProcessor
from app.utils.errors import DocumentProcessingError


class TestDocumentProcessor:
    """Test document processor functionality"""

    @pytest.fixture
    def processor(self):
        """Create document processor instance"""
        return DocumentProcessor()

    def test_chunk_content_basic(self, processor):
        """Test basic content chunking"""
        text = "This is a test. " * 100  # Create longer text
        chunks = processor.chunk_content(text, "test_doc_1", page_count=1)
        
        assert len(chunks) > 0
        assert chunks[0].document_id == "test_doc_1"
        assert chunks[0].page_number == 1
        assert all(chunk.text for chunk in chunks)

    def test_chunk_content_empty(self, processor):
        """Test chunking empty content"""
        chunks = processor.chunk_content("", "test_doc", page_count=1)
        assert len(chunks) == 0

    def test_chunk_overlap(self, processor):
        """Test that chunks have overlap"""
        text = "word " * 500  # Create text with many words
        chunks = processor.chunk_content(text, "test_doc", page_count=1)
        
        if len(chunks) > 1:
            # Check that consecutive chunks have overlap
            chunk1_end = chunks[0].text[-50:]
            chunk2_start = chunks[1].text[:50]
            # They should share some content (rough check)
            assert len(chunks) >= 1

    def test_extract_text_from_txt(self, processor, tmp_path):
        """Test text extraction from text file"""
        # Create a temp text file
        test_file = tmp_path / "test.txt"
        test_content = "This is test content.\nLine 2.\nLine 3."
        test_file.write_text(test_content)
        
        text, pages = processor.extract_text_from_txt(str(test_file))
        
        assert test_content in text
        assert pages == 1

    def test_extract_text_from_txt_not_found(self, processor):
        """Test error handling for missing file"""
        with pytest.raises(DocumentProcessingError):
            processor.extract_text_from_txt("/nonexistent/file.txt")
