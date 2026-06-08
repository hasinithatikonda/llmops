from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.feedback import Feedback
from app.models.response import Response
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from typing import List

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("/", response_model=FeedbackResponse)
async def create_feedback(
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit feedback for a response"""
    
    # Verify response exists and belongs to user
    response = db.query(Response).filter(
        Response.id == feedback_data.response_id,
        Response.user_id == current_user.id
    ).first()
    
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    
    # Check if feedback already exists
    existing_feedback = db.query(Feedback).filter(
        Feedback.response_id == feedback_data.response_id,
        Feedback.user_id == current_user.id
    ).first()
    
    if existing_feedback:
        # Update existing feedback
        existing_feedback.rating = feedback_data.rating
        existing_feedback.comment = feedback_data.comment
        db.commit()
        db.refresh(existing_feedback)
        return existing_feedback
    
    # Create new feedback
    feedback = Feedback(
        response_id=feedback_data.response_id,
        user_id=current_user.id,
        rating=feedback_data.rating,
        comment=feedback_data.comment
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    return feedback

@router.get("/", response_model=List[FeedbackResponse])
async def get_user_feedback(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's feedback history"""
    feedback = db.query(Feedback).filter(
        Feedback.user_id == current_user.id
    ).order_by(Feedback.created_at.desc()).limit(limit).all()
    
    return feedback
