"""Query/QA routes"""

import logging
import time
from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.services.qa_service import QAService
from app.utils.errors import ApplicationError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/queries", tags=["queries"])

# Initialize QA service
qa_service = QAService()


@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest) -> QueryResponse:
    """Ask a question about the document

    Args:
        request: QueryRequest with question and document_id

    Returns:
        QueryResponse with answer and sources

    Raises:
        HTTPException: If query processing fails
    """
    start_time = time.time()

    try:
        logger.info(
            f"Processing query for document: {request.document_id} "
            f"Question: {request.question[:50]}..."
        )

        # Process question
        response = qa_service.answer_question(
            question=request.question,
            document_id=request.document_id
        )

        processing_time = time.time() - start_time
        logger.info(
            f"Query processed in {processing_time:.2f}s "
            f"(Confidence: {response.confidence_score:.2f})"
        )

        return response

    except ApplicationError as e:
        logger.error(f"Application error during query: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Query processing failed"
        )
