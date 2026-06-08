from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FeedbackCreate(BaseModel):
    response_id: int
    rating: int  # 1-5
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    response_id: int
    user_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
