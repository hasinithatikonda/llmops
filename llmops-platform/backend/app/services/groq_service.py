import time
from groq import Groq
from app.core.config import settings

class GroqService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
    
    def generate_completion(
        self, 
        prompt: str, 
        model: str = "mixtral-8x7b-32768",
        temperature: float = 0.7,
        max_tokens: int = 1024
    ):
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            return {
                "content": response.choices[0].message.content,
                "model": response.model,
                "tokens_used": response.usage.total_tokens,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "latency_ms": latency_ms,
                "cost": self.calculate_cost(response.usage.total_tokens, model),
                "is_error": False,
                "error_message": None
            }
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return {
                "content": "",
                "model": model,
                "tokens_used": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "latency_ms": latency_ms,
                "cost": 0.0,
                "is_error": True,
                "error_message": str(e)
            }
    
    def calculate_cost(self, tokens: int, model: str) -> float:
        # Groq pricing (approximate, check current pricing)
        pricing = {
            "mixtral-8x7b-32768": 0.00024 / 1000,  # per token
            "llama2-70b-4096": 0.00070 / 1000,
            "gemma-7b-it": 0.00010 / 1000,
        }
        return tokens * pricing.get(model, 0.0002 / 1000)

groq_service = GroqService()
