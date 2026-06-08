from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.prompt import Prompt
from app.models.response import Response
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.groq_service import groq_service
from app.utils.security_checks import security_checker
from app.utils.rate_limiter import limiter
import uuid

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
@limiter.limit("30/minute")
async def chat(
    request: Request,
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a chat message and get response"""
    
    # Security check
    security_check = security_checker.check_prompt(chat_request.message)
    if not security_check["is_safe"]:
        raise HTTPException(
            status_code=400,
            detail=f"Security issue detected: {', '.join(security_check['issues'])}"
        )
    
    # Sanitize input
    sanitized_message = security_checker.sanitize_input(chat_request.message)
    
    # Generate session ID if not provided
    session_id = chat_request.session_id or str(uuid.uuid4())
    
    # Save prompt
    prompt = Prompt(
        user_id=current_user.id,
        content=sanitized_message,
        model=chat_request.model,
        temperature=str(chat_request.temperature),
        max_tokens=chat_request.max_tokens,
        session_id=session_id
    )
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    
    # Generate response using Groq
    llm_response = groq_service.generate_completion(
        prompt=sanitized_message,
        model=chat_request.model,
        temperature=chat_request.temperature,
        max_tokens=chat_request.max_tokens
    )
    
    # Save response
    response = Response(
        prompt_id=prompt.id,
        user_id=current_user.id,
        content=llm_response["content"],
        model=llm_response["model"],
        tokens_used=llm_response["tokens_used"],
        prompt_tokens=llm_response["prompt_tokens"],
        completion_tokens=llm_response["completion_tokens"],
        latency_ms=llm_response["latency_ms"],
        cost=llm_response["cost"],
        is_error=llm_response["is_error"],
        error_message=llm_response["error_message"],
        session_id=session_id
    )
    db.add(response)
    db.commit()
    db.refresh(response)
    
    # Check for alerts
    if llm_response["latency_ms"] > 3000:
        from app.models.alert import Alert
        alert = Alert(
            type="latency",
            severity="high",
            message=f"High latency detected: {llm_response['latency_ms']:.2f}ms"
        )
        db.add(alert)
        db.commit()
    
    return response

@router.get("/history")
async def get_chat_history(
    session_id: str = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get chat history"""
    query = db.query(Response).filter(Response.user_id == current_user.id)
    
    if session_id:
        query = query.filter(Response.session_id == session_id)
    
    responses = query.order_by(Response.created_at.desc()).limit(limit).all()
    return responses
