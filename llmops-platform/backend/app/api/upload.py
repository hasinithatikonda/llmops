from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.core.security import get_current_user
from app.models.user import User
from app.services.rag_service import rag_service

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Upload and process PDF document"""
    
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Check file size (max 10MB)
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
    
    # Process PDF
    result = rag_service.process_pdf(content, file.filename)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {result['error']}")
    
    return {
        "message": "PDF processed successfully",
        "filename": result["filename"],
        "pages": result["pages"],
        "chunks": result["chunks"]
    }

@router.post("/query")
async def query_documents(
    query: str,
    n_results: int = 3,
    current_user: User = Depends(get_current_user)
):
    """Query documents with RAG"""
    result = rag_service.query_with_context(query, n_results)
    
    return {
        "query": result["query"],
        "response": result["response"]["content"],
        "context": result["context"],
        "latency_ms": result["response"]["latency_ms"]
    }
