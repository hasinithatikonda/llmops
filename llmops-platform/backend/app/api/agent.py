from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.agents.llmops_agent import LLMOpsAgent

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.post("/analyze")
async def analyze_with_agent(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Use LLMOps Agent to analyze metrics"""
    agent = LLMOpsAgent(db)
    result = agent.analyze(query)
    
    return {
        "query": query,
        "analysis": result
    }
