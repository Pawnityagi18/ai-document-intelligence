"""Document upload routes"""

import logging
import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid
from app.services.qa_service import QAService
from app.models.schemas import DocumentUploadResponse
from app.utils.errors import ApplicationError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/documents", tags=["documents"])

# Initialize QA service
qa_service = QAService()

# Store for tracking uploaded documents
uploaded_documents = {}


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)) -> DocumentUploadResponse:
    """Upload and process a document

    Args:
        file: PDF or text file to upload

    Returns:
        DocumentUploadResponse with processing details

    Raises:
        HTTPException: If upload or processing fails
    """
    start_time = time.time()
    temp_file_path = None

    try:
        logger.info(f"Processing upload: {file.filename}")

        # Validate file type
        allowed_extensions = {".pdf", ".txt"}
        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not supported. "
                f"Supported: {', '.join(allowed_extensions)}"
            )

        # Generate document ID
        document_id = str(uuid.uuid4())

        # Save uploaded file temporarily
        temp_dir = Path("temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        temp_file_path = temp_dir / f"{document_id}{file_ext}"

        # Save file
        contents = await file.read()
        with open(temp_file_path, "wb") as f:
            f.write(contents)

        logger.info(f"File saved: {temp_file_path}")

        # Process document
        result = qa_service.process_document(
            file_path=str(temp_file_path),
            document_id=document_id
        )

        # Store document reference
        uploaded_documents[document_id] = {
            "filename": file.filename,
            "file_path": str(temp_file_path),
            "uploaded_at": time.time(),
            "total_chunks": result["total_chunks"]
        }

        processing_time = time.time() - start_time
        logger.info(
            f"Document upload completed: {document_id} "
            f"({processing_time:.2f}s)"
        )

        return DocumentUploadResponse(
            document_id=document_id,
            filename=file.filename,
            total_chunks=result["total_chunks"],
            extracted_text_length=result["extracted_text_length"],
            processing_time_seconds=processing_time,
            message="Document processed successfully"
        )

    except HTTPException:
        raise
    except ApplicationError as e:
        logger.error(f"Application error during upload: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Upload processing failed")
    finally:
        # Cleanup temp file
        if temp_file_path and Path(temp_file_path).exists():
            try:
                Path(temp_file_path).unlink()
                logger.debug(f"Cleaned up temp file: {temp_file_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file: {str(e)}")


@router.get("/status/{document_id}")
async def get_document_status(document_id: str) -> dict:
    """Get status of uploaded document

    Args:
        document_id: ID of the document

    Returns:
        Document status information
    """
    if document_id not in uploaded_documents:
        raise HTTPException(
            status_code=404,
            detail=f"Document {document_id} not found"
        )

    doc_info = uploaded_documents[document_id]
    return {
        "document_id": document_id,
        "filename": doc_info["filename"],
        "total_chunks": doc_info["total_chunks"],
        "status": "ready"
    }
