"""Question-Answering service orchestrating the pipeline"""

import logging
import time
from typing import Dict, Any, List
from app.services.document_processor import DocumentProcessor
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.llm_service import LLMService
from app.config import settings
from app.utils.errors import ApplicationError
from app.models.schemas import QueryResponse, SourceReference

logger = logging.getLogger(__name__)


class QAService:
    """Orchestrate the QA pipeline"""

    def __init__(self):
        """Initialize QA service with all dependencies"""
        self.document_processor = DocumentProcessor()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.llm_service = LLMService()
        self.confidence_threshold = settings.confidence_threshold
        logger.info("Initialized QAService")

    def process_document(
        self,
        file_path: str,
        document_id: str
    ) -> Dict[str, Any]:
        """Process a document end-to-end

        Args:
            file_path: Path to document file
            document_id: ID for the document

        Returns:
            Processing result with metadata
        """
        start_time = time.time()
        logger.info(f"Starting document processing: {file_path}")

        try:
            # Step 1: Extract text
            chunks = self.document_processor.process_document(
                file_path,
                document_id
            )

            if not chunks:
                raise ApplicationError("No chunks created from document")

            # Step 2: Generate embeddings
            logger.info(f"Generating embeddings for {len(chunks)} chunks")
            chunk_texts = [chunk.text for chunk in chunks]
            embeddings = self.embedding_service.generate_embeddings(
                chunk_texts
            )

            # Step 3: Store in vector database
            logger.info("Storing embeddings in vector database")
            metadata = [
                {
                    "page_number": chunk.page_number,
                    "chunk_index": chunk.chunk_index,
                    "source_length": chunk.source_length
                }
                for chunk in chunks
            ]

            self.vector_store.add_documents(
                document_id=document_id,
                texts=chunk_texts,
                embeddings=embeddings,
                metadata=metadata
            )

            processing_time = time.time() - start_time
            logger.info(
                f"Document processing completed in {processing_time:.2f}s: "
                f"{len(chunks)} chunks"
            )

            # Calculate extracted text length
            total_text_length = sum(len(chunk.text) for chunk in chunks)

            return {
                "document_id": document_id,
                "total_chunks": len(chunks),
                "extracted_text_length": total_text_length,
                "processing_time_seconds": processing_time,
                "status": "success"
            }

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(
                f"Document processing failed after {processing_time:.2f}s: "
                f"{str(e)}"
            )
            raise

    def answer_question(
        self,
        question: str,
        document_id: str
    ) -> QueryResponse:
        """Answer a question based on document

        Args:
            question: User question
            document_id: ID of the document to query

        Returns:
            QueryResponse with answer and sources
        """
        start_time = time.time()
        logger.info(f"Processing question: {question[:50]}...")

        try:
            # Step 1: Embed the question
            logger.debug("Embedding question")
            query_embedding = self.embedding_service.generate_embedding(
                question
            )

            # Step 2: Search for similar chunks
            logger.debug("Searching for similar chunks")
            search_results = self.vector_store.search(
                query_embedding=query_embedding,
                k=settings.top_k_results
            )

            if not search_results:
                logger.warning("No search results found")
                answer = (
                    "I don't know. No relevant information was found in "
                    "the document to answer your question."
                )
                confidence = 0.0
                sources = []
                is_confident = False
            else:
                # Step 3: Build context from top results
                context_parts = []
                source_references = []

                for result in search_results:
                    text = result["text"]
                    metadata = result["metadata"]
                    relevance = result["relevance_score"]

                    context_parts.append(f"- {text}")

                    source_references.append(
                        SourceReference(
                            page_number=int(metadata.get("page_number", 1)),
                            chunk_index=int(metadata.get("chunk_index", 0)),
                            text_preview=text[:100],
                            relevance_score=relevance
                        )
                    )

                context = "\n".join(context_parts)

                # Step 4: Generate answer
                logger.debug("Generating answer from context")
                answer, confidence = self.llm_service.generate_answer(
                    question=question,
                    context=context
                )

                # Step 5: Determine if we're confident
                is_confident = (
                    confidence >= self.confidence_threshold
                )
                sources = source_references

            processing_time = time.time() - start_time
            logger.info(
                f"Question answered in {processing_time:.2f}s "
                f"(confidence: {confidence:.2f})"
            )

            return QueryResponse(
                answer=answer,
                confidence_score=confidence,
                sources=sources,
                processing_time_seconds=processing_time,
                is_confident=is_confident
            )

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(
                f"Question processing failed after {processing_time:.2f}s: "
                f"{str(e)}"
            )
            raise
