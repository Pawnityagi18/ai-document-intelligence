"""Document processing service"""

import logging
from pathlib import Path
from typing import List, Tuple
import PyPDF2
from app.models.domain import Chunk
from app.utils.errors import DocumentProcessingError
from app.config import settings

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Process documents and extract text"""

    def __init__(self):
        """Initialize document processor"""
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap

    def extract_text_from_pdf(self, file_path: str) -> Tuple[str, int]:
        """Extract text from PDF file

        Args:
            file_path: Path to PDF file

        Returns:
            Tuple of (extracted_text, page_count)

        Raises:
            DocumentProcessingError: If extraction fails
        """
        try:
            logger.info(f"Extracting text from PDF: {file_path}")
            extracted_text = ""
            page_count = 0

            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page_count = len(pdf_reader.pages)

                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    extracted_text += f"\n[Page {page_num + 1}]\n{text}"

            logger.info(
                f"Successfully extracted {len(extracted_text)} characters "
                f"from {page_count} pages"
            )
            return extracted_text, page_count

        except Exception as e:
            error_msg = f"Failed to extract text from PDF: {str(e)}"
            logger.error(error_msg)
            raise DocumentProcessingError(error_msg) from e

    def extract_text_from_file(self, file_path: str) -> Tuple[str, int]:
        """Extract text from file (PDF or TXT)

        Args:
            file_path: Path to file

        Returns:
            Tuple of (extracted_text, page_count)

        Raises:
            DocumentProcessingError: If extraction fails
        """
        file_ext = Path(file_path).suffix.lower()

        if file_ext == ".pdf":
            return self.extract_text_from_pdf(file_path)
        elif file_ext == ".txt":
            return self.extract_text_from_txt(file_path)
        else:
            raise DocumentProcessingError(
                f"Unsupported file type: {file_ext}. "
                "Supported: .pdf, .txt"
            )

    def extract_text_from_txt(self, file_path: str) -> Tuple[str, int]:
        """Extract text from text file

        Args:
            file_path: Path to text file

        Returns:
            Tuple of (extracted_text, page_count)

        Raises:
            DocumentProcessingError: If extraction fails
        """
        try:
            logger.info(f"Extracting text from file: {file_path}")
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
            logger.info(f"Successfully extracted {len(text)} characters")
            return text, 1  # Treat whole file as single page
        except Exception as e:
            error_msg = f"Failed to extract text from file: {str(e)}"
            logger.error(error_msg)
            raise DocumentProcessingError(error_msg) from e

    def chunk_content(
        self,
        text: str,
        document_id: str,
        page_count: int = 1
    ) -> List[Chunk]:
        """Split content into overlapping chunks

        Args:
            text: Full extracted text
            document_id: ID of the document
            page_count: Total pages in document

        Returns:
            List of Chunk objects
        """
        if not text:
            logger.warning("Empty text provided for chunking")
            return []

        logger.info(
            f"Chunking content: size={self.chunk_size}, "
            f"overlap={self.chunk_overlap}"
        )

        chunks = []
        chunk_index = 0
        start_pos = 0
        text_length = len(text)
        source_length = len(text)

        while start_pos < text_length:
            # Calculate end position
            end_pos = min(start_pos + self.chunk_size, text_length)

            # Extract chunk
            chunk_text = text[start_pos:end_pos]

            # Estimate page number (rough estimate based on position)
            estimated_page = max(
                1,
                min(
                    int((start_pos / text_length) * page_count) + 1,
                    page_count
                )
            )

            # Create chunk object
            chunk = Chunk(
                text=chunk_text,
                page_number=estimated_page,
                chunk_index=chunk_index,
                document_id=document_id,
                source_length=source_length
            )
            chunks.append(chunk)

            # Move start position (with overlap)
            start_pos += (self.chunk_size - self.chunk_overlap)
            chunk_index += 1

        logger.info(
            f"Created {len(chunks)} chunks from "
            f"{text_length} characters"
        )
        return chunks

    def process_document(
        self,
        file_path: str,
        document_id: str
    ) -> List[Chunk]:
        """Process a complete document

        Args:
            file_path: Path to document
            document_id: ID to assign to document

        Returns:
            List of processed chunks

        Raises:
            DocumentProcessingError: If processing fails
        """
        try:
            logger.info(f"Processing document: {file_path}")

            # Extract text
            text, page_count = self.extract_text_from_file(file_path)

            # Create chunks
            chunks = self.chunk_content(text, document_id, page_count)

            logger.info(
                f"Successfully processed document: "
                f"{len(chunks)} chunks created"
            )
            return chunks

        except DocumentProcessingError:
            raise
        except Exception as e:
            error_msg = f"Unexpected error processing document: {str(e)}"
            logger.error(error_msg)
            raise DocumentProcessingError(error_msg) from e
