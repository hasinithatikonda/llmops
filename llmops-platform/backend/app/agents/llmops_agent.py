from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.response import Response
from app.models.prompt import Prompt
from app.models.evaluation import Evaluation
from app.services.groq_service import groq_service
from datetime import datetime, timedelta
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    analysis_type: str
    data: dict

class LLMOpsAgent:
    """LangGraph-based LLMOps Analyst Agent"""
    
    def __init__(self, db: Session):
        self.db = db
        self.graph = self._build_graph()
    
    def _build_graph(self):
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_request", self.analyze_request)
        workflow.add_node("fetch_data", self.fetch_data)
        workflow.add_node("generate_insights", self.generate_insights)
        workflow.add_node("format_response", self.format_response)
        
        # Add edges
        workflow.set_entry_point("analyze_request")
        workflow.add_edge("analyze_request", "fetch_data")
        workflow.add_edge("fetch_data", "generate_insights")
        workflow.add_edge("generate_insights", "format_response")
        workflow.add_edge("format_response", END)
        
        return workflow.compile()
    
    def analyze_request(self, state: AgentState) -> AgentState:
        """Analyze the user request to determine analysis type"""
        user_message = state["messages"][-1].content.lower()
        
        if any(word in user_message for word in ["latency", "slow", "performance"]):
            analysis_type = "latency"
        elif any(word in user_message for word in ["cost", "expensive", "spending"]):
            analysis_type = "cost"
        elif any(word in user_message for word in ["error", "failure", "failed"]):
            analysis_type = "error"
        elif any(word in user_message for word in ["quality", "evaluation", "ragas"]):
            analysis_type = "quality"
        else:
            analysis_type = "general"
        
        state["analysis_type"] = analysis_type
        return state
    
    def fetch_data(self, state: AgentState) -> AgentState:
        """Fetch relevant data based on analysis type"""
        analysis_type = state["analysis_type"]
        data = {}
        
        # Last 24 hours
        time_filter = datetime.utcnow() - timedelta(days=1)
        
        if analysis_type == "latency":
            # Get high latency queries
            high_latency = self.db.query(Response).filter(
                Response.created_at >= time_filter,
                Response.latency_ms > 2000
            ).order_by(desc(Response.latency_ms)).limit(10).all()
            
            data["high_latency_count"] = len(high_latency)
            data["avg_latency"] = self.db.query(func.avg(Response.latency_ms)).filter(
                Response.created_at >= time_filter
            ).scalar()
            data["max_latency"] = self.db.query(func.max(Response.latency_ms)).filter(
                Response.created_at >= time_filter
            ).scalar()
        
        elif analysis_type == "cost":
            total_cost = self.db.query(func.sum(Response.cost)).filter(
                Response.created_at >= time_filter
            ).scalar() or 0
            
            total_tokens = self.db.query(func.sum(Response.tokens_used)).filter(
                Response.created_at >= time_filter
            ).scalar() or 0
            
            data["total_cost"] = total_cost
            data["total_tokens"] = total_tokens
            data["requests"] = self.db.query(Response).filter(
                Response.created_at >= time_filter
            ).count()
        
        elif analysis_type == "error":
            errors = self.db.query(Response).filter(
                Response.created_at >= time_filter,
                Response.is_error == True
            ).all()
            
            data["error_count"] = len(errors)
            data["error_rate"] = (len(errors) / max(self.db.query(Response).count(), 1)) * 100
            data["error_messages"] = list(set([e.error_message for e in errors if e.error_message]))[:5]
        
        elif analysis_type == "quality":
            evaluations = self.db.query(Evaluation).join(Response).filter(
                Response.created_at >= time_filter
            ).all()
            
            if evaluations:
                data["avg_faithfulness"] = sum([e.faithfulness or 0 for e in evaluations]) / len(evaluations)
                data["avg_relevance"] = sum([e.relevance or 0 for e in evaluations]) / len(evaluations)
                data["avg_ragas"] = sum([e.ragas_score or 0 for e in evaluations]) / len(evaluations)
                data["evaluation_count"] = len(evaluations)
        
        else:
            # General metrics
            data["total_requests"] = self.db.query(Response).filter(
                Response.created_at >= time_filter
            ).count()
            data["avg_latency"] = self.db.query(func.avg(Response.latency_ms)).filter(
                Response.created_at >= time_filter
            ).scalar()
            data["total_cost"] = self.db.query(func.sum(Response.cost)).filter(
                Response.created_at >= time_filter
            ).scalar() or 0
        
        state["data"] = data
        return state
    
    def generate_insights(self, state: AgentState) -> AgentState:
        """Generate insights using Groq"""
        analysis_type = state["analysis_type"]
        data = state["data"]
        
        prompt = f"""You are an LLMOps analyst. Analyze the following {analysis_type} data and provide insights:

Data: {data}

Provide:
1. Summary of findings
2. Potential issues or concerns
3. Actionable recommendations
4. Optimization suggestions

Keep it concise and actionable."""
        
        response = groq_service.generate_completion(prompt, temperature=0.3, max_tokens=500)
        
        state["messages"].append(AIMessage(content=response["content"]))
        return state
    
    def format_response(self, state: AgentState) -> AgentState:
        """Format the final response"""
        # The last message already contains the formatted response
        return state
    
    def analyze(self, query: str) -> str:
        """Run the analysis"""
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "analysis_type": "",
            "data": {}
        }
        
        final_state = self.graph.invoke(initial_state)
        return final_state["messages"][-1].content
