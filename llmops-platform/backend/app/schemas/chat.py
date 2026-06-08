from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    model: str = "mixtral-8x7b-32768"
    temperature: float = 0.7
    max_tokens: int = 1024
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    id: int
    prompt_id: int
    content: str
    model: str
    tokens_used: int
    latency_ms: float
    cost: float
    session_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PromptResponse(BaseModel):
    id: int
    content: str
    model: str
    session_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
