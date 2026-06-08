from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.database import engine, Base
from app.utils.rate_limiter import limiter
from app.api import auth, chat, upload, metrics, feedback, alerts, agent, evaluation

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LLMOps Monitoring Platform",
    description="Production-ready LLMOps monitoring and evaluation platform",
    version="1.0.0"
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(metrics.router)
app.include_router(feedback.router)
app.include_router(alerts.router)
app.include_router(agent.router)
app.include_router(evaluation.router)

@app.get("/")
async def root():
    return {
        "message": "LLMOps Monitoring Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
