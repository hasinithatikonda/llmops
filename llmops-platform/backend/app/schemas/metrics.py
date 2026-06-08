from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MetricsSummary(BaseModel):
    total_requests: int
    active_users: int
    average_latency: float
    error_rate: float
    total_tokens: int
    total_cost: float
    average_feedback_score: Optional[float]

class UsageMetrics(BaseModel):
    date: str
    requests: int
    tokens: int
    cost: float
    avg_latency: float

class ModelMetrics(BaseModel):
    model: str
    requests: int
    tokens: int
    avg_latency: float
    error_rate: float

class EvaluationMetrics(BaseModel):
    avg_faithfulness: Optional[float]
    avg_relevance: Optional[float]
    avg_context_precision: Optional[float]
    avg_context_recall: Optional[float]
    avg_hallucination_risk: Optional[float]
    avg_ragas_score: Optional[float]
