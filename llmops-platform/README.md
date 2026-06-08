# LLMOps Monitoring Platform

A production-ready LLMOps monitoring and evaluation platform built with Next.js, FastAPI, PostgreSQL, ChromaDB, LangGraph, Groq API, LangSmith, and RAGAS.

## Features

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (Admin/User)
- Secure password hashing with bcrypt

### LLM Monitoring
- Track all prompts and responses
- Monitor token usage and costs
- Measure response latency
- Error logging and alerting
- User feedback collection

### Analytics Dashboard
- Total requests and active users
- Average latency and error rates
- Token usage and cost tracking
- Model performance comparison
- RAGAS evaluation metrics

### RAG Pipeline
- PDF document upload and processing
- Automatic document chunking
- Vector storage with ChromaDB
- Semantic search and retrieval
- Context-aware responses

### LangGraph Agent
- LLMOps Analyst Agent
- Automated latency analysis
- Cost optimization suggestions
- Error pattern detection
- Performance insights

### Security
- Prompt injection detection
- Input validation and sanitization
- Rate limiting
- API key protection
- Audit logging

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Vector DB**: ChromaDB
- **LLM**: Groq API
- **Agent Framework**: LangGraph
- **Evaluation**: LangSmith, RAGAS
- **Authentication**: JWT (python-jose)

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Icons**: Lucide React

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Redis (for rate limiting)
- Groq API key
- LangSmith API key (optional)

## Local Development Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd llmops-platform
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API keys and database URL

# Run the backend
uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env.local

# Run the frontend
npm run dev
```

Frontend will run on `http://localhost:3000`

### 4. Database Setup

```bash
# Using Docker
docker run --name llmops-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=llmops_db -p 5432:5432 -d postgres:15

# Or use docker-compose (includes Redis)
docker-compose up -d postgres redis
```

## Docker Deployment

### Using Docker Compose (Recommended for local testing)

```bash
# Create .env file
cp .env.example .env
# Edit .env and add your API keys

# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Production Deployment

### Backend - Deploy to Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3.11
4. Add environment variables:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `SECRET_KEY`: Random secret key
   - `GROQ_API_KEY`: Your Groq API key
   - `LANGSMITH_API_KEY`: Your LangSmith API key
   - `FRONTEND_URL`: Your frontend URL
5. Add PostgreSQL database addon

### Frontend - Deploy to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. From the frontend directory:
   ```bash
   cd frontend
   vercel
   ```
3. Set environment variable:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL
4. Deploy: `vercel --prod`

### CI/CD with GitHub Actions

1. Add GitHub secrets:
   - `RENDER_SERVICE_ID`
   - `RENDER_API_KEY`
   - `VERCEL_TOKEN`
   - `VERCEL_ORG_ID`
   - `VERCEL_PROJECT_ID`

2. Push to main branch to trigger deployment

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user

#### Chat
- `POST /chat/` - Send chat message
- `GET /chat/history` - Get chat history

#### Metrics
- `GET /metrics/summary` - Get metrics summary
- `GET /metrics/usage` - Get usage metrics
- `GET /metrics/models` - Get model metrics
- `GET /metrics/evaluation` - Get evaluation metrics

#### Upload & RAG
- `POST /upload/pdf` - Upload PDF document
- `POST /upload/query` - Query documents with RAG

#### Feedback
- `POST /feedback/` - Submit feedback
- `GET /feedback/` - Get feedback history

#### Alerts
- `GET /alerts/` - Get alerts
- `PATCH /alerts/{id}/resolve` - Resolve alert

#### Agent
- `POST /agent/analyze` - Analyze with LLMOps agent

## Database Schema

### users
- id, email, username, hashed_password, role, is_active, created_at

### prompts
- id, user_id, content, model, temperature, max_tokens, session_id, created_at

### responses
- id, prompt_id, user_id, content, model, tokens_used, latency_ms, cost, is_error, session_id, created_at

### feedback
- id, response_id, user_id, rating, comment, created_at

### evaluations
- id, response_id, faithfulness, relevance, context_precision, context_recall, hallucination_risk, ragas_score, created_at

### alerts
- id, type, severity, message, is_resolved, created_at, resolved_at

### audit_logs
- id, user_id, action, resource, details, ip_address, user_agent, created_at

## Configuration

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/llmops_db
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
LANGSMITH_API_KEY=your-langsmith-api-key
CHROMA_PERSIST_DIR=./chroma_db
REDIS_URL=redis://localhost:6379
FRONTEND_URL=http://localhost:3000
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Security Features

1. **Authentication**: JWT tokens with expiration
2. **Password Hashing**: bcrypt with salt
3. **Input Validation**: Pydantic models
4. **Prompt Injection Detection**: Pattern matching
5. **Rate Limiting**: SlowAPI with Redis
6. **CORS**: Configured for specific origins
7. **Audit Logging**: All actions logged

## Monitoring & Evaluation

### Metrics Tracked
- Total requests and active users
- Token usage and costs
- Average latency and error rates
- Model performance comparison

### RAGAS Metrics
- Faithfulness: Answer consistency with context
- Relevance: Answer relevance to question
- Context Precision: Context relevance
- Context Recall: Context completeness
- Hallucination Risk: Factual accuracy

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Test connection
psql -h localhost -U llmops_user -d llmops_db
```

### ChromaDB Issues
```bash
# Clear ChromaDB
rm -rf backend/chroma_db
```

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Support

For issues and questions, please open a GitHub issue.

## Roadmap

- [ ] Multi-model support
- [ ] Real-time monitoring dashboard
- [ ] Advanced analytics
- [ ] A/B testing support
- [ ] Custom evaluation metrics
- [ ] Slack/Email notifications
- [ ] Data export functionality
- [ ] Advanced RAG techniques

## Acknowledgments

- Groq for fast LLM inference
- LangChain for RAG pipeline
- LangGraph for agent orchestration
- RAGAS for evaluation framework
- FastAPI for backend framework
- Next.js for frontend framework
