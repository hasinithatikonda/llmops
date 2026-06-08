# Project Structure

```
llmops-platform/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── api/                      # API Routes
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # Authentication endpoints
│   │   │   ├── chat.py              # Chat endpoints
│   │   │   ├── upload.py            # PDF upload & RAG
│   │   │   ├── metrics.py           # Metrics endpoints
│   │   │   ├── feedback.py          # Feedback endpoints
│   │   │   ├── alerts.py            # Alerts management
│   │   │   ├── agent.py             # LangGraph agent
│   │   │   └── evaluation.py        # RAGAS evaluation
│   │   │
│   │   ├── core/                     # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # Configuration
│   │   │   ├── database.py          # Database setup
│   │   │   └── security.py          # JWT & password handling
│   │   │
│   │   ├── models/                   # SQLAlchemy Models
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User model
│   │   │   ├── prompt.py            # Prompt model
│   │   │   ├── response.py          # Response model
│   │   │   ├── feedback.py          # Feedback model
│   │   │   ├── evaluation.py        # Evaluation model
│   │   │   ├── alert.py             # Alert model
│   │   │   └── audit_log.py         # Audit log model
│   │   │
│   │   ├── schemas/                  # Pydantic Schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User schemas
│   │   │   ├── chat.py              # Chat schemas
│   │   │   ├── feedback.py          # Feedback schemas
│   │   │   └── metrics.py           # Metrics schemas
│   │   │
│   │   ├── services/                 # Business Logic
│   │   │   ├── __init__.py
│   │   │   ├── groq_service.py      # Groq API integration
│   │   │   ├── chroma_service.py    # ChromaDB operations
│   │   │   ├── rag_service.py       # RAG pipeline
│   │   │   └── evaluation_service.py # RAGAS evaluation
│   │   │
│   │   ├── agents/                   # LangGraph Agents
│   │   │   ├── __init__.py
│   │   │   └── llmops_agent.py      # LLMOps analyst agent
│   │   │
│   │   ├── utils/                    # Utilities
│   │   │   ├── __init__.py
│   │   │   ├── rate_limiter.py      # Rate limiting
│   │   │   └── security_checks.py   # Security validation
│   │   │
│   │   └── main.py                   # FastAPI application
│   │
│   ├── chroma_db/                    # ChromaDB persistence
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Docker configuration
│   ├── .dockerignore
│   ├── .env.example
│   ├── alembic.ini                   # Database migrations
│   └── render.yaml                   # Render deployment config
│
├── frontend/                         # Next.js Frontend
│   ├── src/
│   │   ├── app/                      # App Router
│   │   │   ├── page.tsx             # Home page
│   │   │   ├── layout.tsx           # Root layout
│   │   │   ├── globals.css          # Global styles
│   │   │   ├── login/
│   │   │   │   └── page.tsx         # Login page
│   │   │   ├── register/
│   │   │   │   └── page.tsx         # Register page
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx         # Dashboard page
│   │   │   ├── chat/
│   │   │   │   └── page.tsx         # Chat page
│   │   │   └── upload/
│   │   │       └── page.tsx         # Upload page
│   │   │
│   │   ├── components/               # React Components
│   │   │   └── Navbar.tsx           # Navigation component
│   │   │
│   │   ├── lib/                      # Utilities
│   │   │   ├── api.ts               # API client
│   │   │   └── auth.ts              # Auth service
│   │   │
│   │   └── types/                    # TypeScript types
│   │       └── index.ts             # Type definitions
│   │
│   ├── public/                       # Static assets
│   ├── package.json                  # Node dependencies
│   ├── tsconfig.json                 # TypeScript config
│   ├── tailwind.config.js            # Tailwind config
│   ├── next.config.js                # Next.js config
│   ├── postcss.config.js             # PostCSS config
│   ├── Dockerfile                    # Docker configuration
│   ├── .dockerignore
│   ├── .env.example
│   └── vercel.json                   # Vercel deployment config
│
├── .github/
│   └── workflows/
│       └── deploy.yml                # CI/CD workflow
│
├── docker-compose.yml                # Docker Compose config
├── .gitignore                        # Git ignore rules
├── .env.example                      # Environment variables
├── .env.production.example           # Production env vars
├── README.md                         # Main documentation
├── QUICKSTART.md                     # Quick start guide
├── ARCHITECTURE.md                   # Architecture docs
├── DEPLOYMENT.md                     # Deployment guide
├── PROJECT_STRUCTURE.md              # This file
├── CONTRIBUTING.md                   # Contribution guide
└── LICENSE                           # MIT License
```

## Key Files Explained

### Backend

**app/main.py**
- FastAPI application entry point
- CORS configuration
- Route registration
- Database initialization

**app/core/config.py**
- Environment variables
- Application settings
- Configuration management

**app/core/security.py**
- JWT token generation/verification
- Password hashing
- User authentication

**app/services/groq_service.py**
- Groq API integration
- Token tracking
- Cost calculation

**app/services/rag_service.py**
- PDF processing
- Text chunking
- Context retrieval

**app/agents/llmops_agent.py**
- LangGraph agent implementation
- Automated analysis
- Insight generation

### Frontend

**src/app/layout.tsx**
- Root layout component
- Global styles
- Metadata configuration

**src/app/dashboard/page.tsx**
- Main analytics dashboard
- Metrics visualization
- Charts and graphs

**src/lib/api.ts**
- Axios configuration
- Request/response interceptors
- Auth token handling

**src/lib/auth.ts**
- Authentication service
- Login/logout functions
- Token management

### Configuration Files

**docker-compose.yml**
- PostgreSQL service
- Redis service
- Backend service
- Frontend service

**backend/requirements.txt**
- FastAPI and dependencies
- Database drivers
- LLM libraries

**frontend/package.json**
- Next.js and React
- Tailwind CSS
- Chart libraries

## Module Dependencies

### Backend Dependencies
```
FastAPI → SQLAlchemy → PostgreSQL
FastAPI → Groq → LLM Responses
FastAPI → ChromaDB → Vector Storage
FastAPI → Redis → Rate Limiting
LangGraph → Groq → Agent Analysis
```

### Frontend Dependencies
```
Next.js → React → UI Components
Axios → FastAPI → Backend API
Recharts → Data → Visualizations
```

## Data Flow

### Authentication
```
User Input → Frontend → /auth/login → Backend
Backend → Verify → Generate JWT → Return Token
Frontend → Store Token → Protected Routes
```

### Chat
```
User Message → Frontend → /chat → Backend
Backend → Security Check → Groq API
Groq → Response → Save to DB → Return
Frontend → Display → Update UI
```

### RAG
```
PDF Upload → Frontend → /upload/pdf → Backend
Backend → Parse PDF → Chunk → ChromaDB
Query → Frontend → /upload/query → Backend
Backend → Retrieve Context → Groq → Return
```

### Metrics
```
Dashboard Load → Frontend → /metrics/* → Backend
Backend → Query DB → Calculate → Return
Frontend → Recharts → Visualize
```

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL connection
- `GROQ_API_KEY`: Groq API key
- `SECRET_KEY`: JWT secret
- `REDIS_URL`: Redis connection

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API URL

## Deployment Structure

### Development
```
localhost:3000 (Frontend)
localhost:8000 (Backend)
localhost:5432 (PostgreSQL)
localhost:6379 (Redis)
```

### Production
```
Vercel (Frontend)
Render (Backend)
Render (PostgreSQL)
Render (Redis)
```

## Database Schema

See models/ directory for full schema.

Key tables:
- `users`: User accounts
- `prompts`: User prompts
- `responses`: LLM responses
- `feedback`: User feedback
- `evaluations`: RAGAS metrics
- `alerts`: System alerts
- `audit_logs`: Audit trail

## API Endpoints

See `/docs` endpoint for full API documentation.

Main routes:
- `/auth/*`: Authentication
- `/chat/*`: Chat functionality
- `/upload/*`: Document upload
- `/metrics/*`: Analytics
- `/feedback/*`: Feedback
- `/alerts/*`: Alerts
- `/agent/*`: Agent analysis
- `/evaluation/*`: Evaluations
