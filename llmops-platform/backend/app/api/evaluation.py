from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.evaluation_service import evaluation_service
from typing import Optional

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])

@router.post("/{response_id}")
async def evaluate_response(
    response_id: int,
    context: Optional[str] = None,
    ground_truth: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Evaluate a response using RAGAS-like metrics"""
    service = evaluation_service(db)
    result = service.evaluate_response(response_id, context, ground_truth)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result

@router.get("/{response_id}")
async def get_evaluation(
    response_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get evaluation for a response"""
    from app.models.evaluation import Evaluation
    
    evaluation = db.query(Evaluation).filter(
        Evaluation.response_id == response_id
    ).first()
    
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    return evaluation
