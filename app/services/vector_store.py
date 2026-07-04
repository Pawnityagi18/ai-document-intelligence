"""Vector store service using ChromaDB"""

import logging
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings
from app.utils.errors import VectorStoreError

logger = logging.getLogger(__name__)


class VectorStore:
    """Manage vector embeddings in ChromaDB"""

    def __init__(self):
        """Initialize vector store"""
        try:
            logger.info(f"Initializing ChromaDB at {settings.chroma_db_path}")

            chroma_settings = ChromaSettings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=settings.chroma_db_path,
                anonymized_telemetry=False
            )

            self.client = chromadb.Client(chroma_settings)
            self.collection_name = settings.chroma_collection_name
            logger.info("ChromaDB client initialized successfully")

        except Exception as e:
            error_msg = f"Failed to initialize ChromaDB: {str(e)}"
            logger.error(error_msg)
            raise VectorStoreError(error_msg) from e

    def add_documents(
        self,
        document_id: str,
        texts: List[str],
        embeddings: List[List[float]],
        metadata: List[Dict[str, Any]]
    ) -> None:
        """Add documents to vector store

        Args:
            document_id: ID of the document
            texts: List of text chunks
            embeddings: List of embedding vectors
            metadata: List of metadata dictionaries

        Raises:
            VectorStoreError: If operation fails
        """
        try:
            logger.info(
                f"Adding {len(texts)} documents to collection "
                f"for document_id: {document_id}"
            )

            # Get or create collection
            collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )

            # Prepare IDs
            ids = [
                f"{document_id}_chunk_{i}" 
                for i in range(len(texts))
            ]

            # Add documents
            collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadata,
                documents=texts
            )

            logger.info(
                f"Successfully added {len(texts)} documents "
                f"to collection"
            )

        except Exception as e:
            error_msg = f"Failed to add documents to vector store: {str(e)}"
            logger.error(error_msg)
            raise VectorStoreError(error_msg) from e

    def search(
        self,
        query_embedding: List[float],
        k: int = None,
        document_id: str = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents

        Args:
            query_embedding: Query embedding vector
            k: Number of results to return (default from config)
            document_id: Filter by document_id (optional)

        Returns:
            List of search results with metadata

        Raises:
            VectorStoreError: If search fails
        """
        try:
            if k is None:
                k = settings.top_k_results

            logger.debug(f"Searching for {k} similar documents")

            collection = self.client.get_collection(
                name=self.collection_name
            )

            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=k
            )

            # Format results
            formatted_results = []
            if results["documents"] and len(results["documents"]) > 0:
                for i, doc in enumerate(results["documents"][0]):
                    distance = results["distances"][0][i]
                    metadata = results["metadatas"][0][i]

                    formatted_results.append({
                        "text": doc,
                        "distance": distance,
                        "relevance_score": 1 - distance,  # Convert distance to similarity
                        "metadata": metadata
                    })

            logger.debug(f"Found {len(formatted_results)} similar documents")
            return formatted_results

        except Exception as e:
            error_msg = f"Failed to search vector store: {str(e)}"
            logger.error(error_msg)
            raise VectorStoreError(error_msg) from e

    def delete_collection(self) -> None:
        """Delete the collection

        Raises:
            VectorStoreError: If deletion fails
        """
        try:
            logger.info("Deleting collection")
            self.client.delete_collection(name=self.collection_name)
            logger.info("Collection deleted successfully")
        except Exception as e:
            error_msg = f"Failed to delete collection: {str(e)}"
            logger.error(error_msg)
            raise VectorStoreError(error_msg) from e

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics

        Returns:
            Dictionary with collection stats
        """
        try:
            collection = self.client.get_collection(
                name=self.collection_name
            )
            count = collection.count()
            return {"document_count": count}
        except Exception as e:
            logger.warning(f"Failed to get collection stats: {str(e)}")
            return {"document_count": 0}
