"""Custom exception classes"""


class ApplicationError(Exception):
    """Base exception for the application"""
    pass


class DocumentProcessingError(ApplicationError):
    """Raised when document processing fails"""
    pass


class EmbeddingError(ApplicationError):
    """Raised when embedding generation fails"""
    pass


class VectorStoreError(ApplicationError):
    """Raised when vector store operations fail"""
    pass


class LLMError(ApplicationError):
    """Raised when LLM operations fail"""
    pass


class ConfigurationError(ApplicationError):
    """Raised when configuration is invalid"""
    pass
