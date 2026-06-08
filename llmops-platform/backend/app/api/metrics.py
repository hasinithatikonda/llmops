from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, Integer
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.response import Response
from app.models.prompt import Prompt
from app.models.evaluation import Evaluation
from app.models.feedback import Feedback
from app.schemas.metrics import MetricsSummary, UsageMetrics, ModelMetrics, EvaluationMetrics
from typing import List

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/summary", response_model=MetricsSummary)
async def get_metrics_summary(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get overall metrics summary"""
    time_filter = datetime.utcnow() - timedelta(days=days)
    
    total_requests = db.query(Response).filter(Response.created_at >= time_filter).count()
    active_users = db.query(func.count(func.distinct(Response.user_id))).filter(
        Response.created_at >= time_filter
    ).scalar()
    
    avg_latency = db.query(func.avg(Response.latency_ms)).filter(
        Response.created_at >= time_filter
    ).scalar() or 0
    
    error_count = db.query(Response).filter(
        Response.created_at >= time_filter,
        Response.is_error == True
    ).count()
    error_rate = (error_count / max(total_requests, 1)) * 100
    
    total_tokens = db.query(func.sum(Response.tokens_used)).filter(
        Response.created_at >= time_filter
    ).scalar() or 0
    
    total_cost = db.query(func.sum(Response.cost)).filter(
        Response.created_at >= time_filter
    ).scalar() or 0
    
    avg_feedback = db.query(func.avg(Feedback.rating)).join(Response).filter(
        Response.created_at >= time_filter
    ).scalar()
    
    return {
        "total_requests": total_requests,
        "active_users": active_users,
        "average_latency": round(avg_latency, 2),
        "error_rate": round(error_rate, 2),
        "total_tokens": total_tokens,
        "total_cost": round(total_cost, 4),
        "average_feedback_score": round(avg_feedback, 2) if avg_feedback else None
    }

@router.get("/usage", response_model=List[UsageMetrics])
async def get_usage_metrics(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get daily usage metrics"""
    time_filter = datetime.utcnow() - timedelta(days=days)
    
    # Group by date
    results = db.query(
        func.date(Response.created_at).label("date"),
        func.count(Response.id).label("requests"),
        func.sum(Response.tokens_used).label("tokens"),
        func.sum(Response.cost).label("cost"),
        func.avg(Response.latency_ms).label("avg_latency")
    ).filter(
        Response.created_at >= time_filter
    ).group_by(
        func.date(Response.created_at)
    ).order_by(
        func.date(Response.created_at)
    ).all()
    
    return [
        {
            "date": str(r.date),
            "requests": r.requests,
            "tokens": r.tokens or 0,
            "cost": round(r.cost or 0, 4),
            "avg_latency": round(r.avg_latency or 0, 2)
        }
        for r in results
    ]

@router.get("/models", response_model=List[ModelMetrics])
async def get_model_metrics(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get metrics by model"""
    time_filter = datetime.utcnow() - timedelta(days=days)
    
    results = db.query(
        Response.model,
        func.count(Response.id).label("requests"),
        func.sum(Response.tokens_used).label("tokens"),
        func.avg(Response.latency_ms).label("avg_latency"),
        (func.sum(func.cast(Response.is_error, Integer)) * 100.0 / func.count(Response.id)).label("error_rate")
    ).filter(
        Response.created_at >= time_filter
    ).group_by(
        Response.model
    ).all()
    
    return [
        {
            "model": r.model,
            "requests": r.requests,
            "tokens": r.tokens or 0,
            "avg_latency": round(r.avg_latency or 0, 2),
            "error_rate": round(r.error_rate or 0, 2)
        }
        for r in results
    ]

@router.get("/evaluation", response_model=EvaluationMetrics)
async def get_evaluation_metrics(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get evaluation metrics"""
    time_filter = datetime.utcnow() - timedelta(days=days)
    
    result = db.query(
        func.avg(Evaluation.faithfulness).label("avg_faithfulness"),
        func.avg(Evaluation.relevance).label("avg_relevance"),
        func.avg(Evaluation.context_precision).label("avg_context_precision"),
        func.avg(Evaluation.context_recall).label("avg_context_recall"),
        func.avg(Evaluation.hallucination_risk).label("avg_hallucination_risk"),
        func.avg(Evaluation.ragas_score).label("avg_ragas_score")
    ).join(Response).filter(
        Response.created_at >= time_filter
    ).first()
    
    return {
        "avg_faithfulness": round(result.avg_faithfulness, 3) if result.avg_faithfulness else None,
        "avg_relevance": round(result.avg_relevance, 3) if result.avg_relevance else None,
        "avg_context_precision": round(result.avg_context_precision, 3) if result.avg_context_precision else None,
        "avg_context_recall": round(result.avg_context_recall, 3) if result.avg_context_recall else None,
        "avg_hallucination_risk": round(result.avg_hallucination_risk, 3) if result.avg_hallucination_risk else None,
        "avg_ragas_score": round(result.avg_ragas_score, 3) if result.avg_ragas_score else None
    }
