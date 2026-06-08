from typing import Dict, Optional
from sqlalchemy.orm import Session
from app.models.evaluation import Evaluation
from app.models.response import Response

class EvaluationService:
    """Service for evaluating LLM responses using RAGAS-like metrics"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def evaluate_response(
        self,
        response_id: int,
        context: Optional[str] = None,
        ground_truth: Optional[str] = None
    ) -> Dict:
        """
        Evaluate a response using multiple metrics
        
        In production, this would use RAGAS library.
        For this implementation, we provide a simplified version.
        """
        response = self.db.query(Response).filter(Response.id == response_id).first()
        
        if not response:
            return {"error": "Response not found"}
        
        # Simplified evaluation (in production, use RAGAS)
        faithfulness = self._calculate_faithfulness(response.content, context)
        relevance = self._calculate_relevance(response.content, context)
        context_precision = self._calculate_context_precision(context)
        context_recall = self._calculate_context_recall(response.content, context)
        hallucination_risk = self._calculate_hallucination_risk(response.content, context)
        
        # Calculate overall RAGAS score
        ragas_score = (faithfulness + relevance + context_precision + context_recall) / 4
        
        # Save evaluation
        evaluation = Evaluation(
            response_id=response_id,
            faithfulness=faithfulness,
            relevance=relevance,
            context_precision=context_precision,
            context_recall=context_recall,
            hallucination_risk=hallucination_risk,
            ragas_score=ragas_score,
            langsmith_data={}
        )
        self.db.add(evaluation)
        self.db.commit()
        
        return {
            "faithfulness": faithfulness,
            "relevance": relevance,
            "context_precision": context_precision,
            "context_recall": context_recall,
            "hallucination_risk": hallucination_risk,
            "ragas_score": ragas_score
        }
    
    def _calculate_faithfulness(self, response: str, context: Optional[str]) -> float:
        """
        Simplified faithfulness calculation
        In production, use RAGAS library for accurate metrics
        """
        if not context:
            return 0.5
        
        # Simple heuristic: check if key phrases from context appear in response
        response_lower = response.lower()
        context_lower = context.lower()
        
        context_words = set(context_lower.split())
        response_words = set(response_lower.split())
        
        overlap = len(context_words.intersection(response_words))
        score = min(overlap / max(len(context_words), 1), 1.0)
        
        return round(score, 3)
    
    def _calculate_relevance(self, response: str, context: Optional[str]) -> float:
        """Simplified relevance calculation"""
        if not context:
            return 0.5
        
        # Simple length-based heuristic
        response_len = len(response.split())
        context_len = len(context.split()) if context else 1
        
        # Penalize very short or very long responses
        ratio = response_len / context_len
        if ratio < 0.1 or ratio > 5.0:
            return 0.3
        
        return 0.8
    
    def _calculate_context_precision(self, context: Optional[str]) -> float:
        """Simplified context precision"""
        if not context:
            return 0.0
        
        # Simple heuristic based on context length
        context_len = len(context.split())
        if context_len < 50:
            return 0.9
        elif context_len < 200:
            return 0.8
        else:
            return 0.7
    
    def _calculate_context_recall(self, response: str, context: Optional[str]) -> float:
        """Simplified context recall"""
        if not context:
            return 0.0
        
        # Check if response references the context
        response_lower = response.lower()
        context_lower = context.lower()
        
        context_sentences = context_lower.split('.')
        referenced = sum(1 for sent in context_sentences if any(word in response_lower for word in sent.split()))
        
        score = referenced / max(len(context_sentences), 1)
        return round(min(score, 1.0), 3)
    
    def _calculate_hallucination_risk(self, response: str, context: Optional[str]) -> float:
        """Simplified hallucination risk calculation"""
        if not context:
            return 0.5
        
        # Check for phrases that indicate uncertainty or hallucination
        risk_phrases = [
            "i think", "i believe", "probably", "maybe", 
            "not sure", "could be", "might be"
        ]
        
        response_lower = response.lower()
        risk_count = sum(1 for phrase in risk_phrases if phrase in response_lower)
        
        # Higher risk if many uncertain phrases
        risk = min(risk_count * 0.2, 1.0)
        return round(risk, 3)

evaluation_service = EvaluationService
