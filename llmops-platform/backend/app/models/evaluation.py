from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Evaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("responses.id"), nullable=False)
    faithfulness = Column(Float)
    relevance = Column(Float)
    context_precision = Column(Float)
    context_recall = Column(Float)
    hallucination_risk = Column(Float)
    ragas_score = Column(Float)
    langsmith_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
