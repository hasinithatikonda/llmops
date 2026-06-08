# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Browser                            │
│                     (Next.js Frontend)                           │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTPS
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                     FastAPI Backend                              │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Auth Router  │  │ Chat Router  │  │Upload Router │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                   │
│  ┌──────▼──────────────────▼──────────────────▼────────┐        │
│  │              Service Layer                           │        │
│  │  • Groq Service  • RAG Service  • Security Checker  │        │
│  └──────┬──────────────────┬──────────────────┬────────┘        │
│         │                  │                  │                   │
└─────────┼──────────────────┼──────────────────┼──────────────────┘
          │                  │                  │
    ┌─────▼─────┐     ┌─────▼─────┐     ┌─────▼─────┐
    │PostgreSQL │     │ ChromaDB  │     │  Groq API │
    │ Database  │     │  Vector   │     │    LLM    │
    └───────────┘     └───────────┘     └───────────┘
```

## Component Breakdown

### Frontend (Next.js 14)

#### Pages
- `/` - Landing/redirect page
- `/login` - Authentication page
- `/register` - User registration
- `/dashboard` - Analytics dashboard
- `/chat` - Chat interface
- `/upload` - Document upload and RAG

#### Components
- `Navbar` - Navigation component
- Chart components (via Recharts)

#### Libraries
- **axios** - HTTP client
- **recharts** - Data visualization
- **lucide-react** - Icons
- **tailwindcss** - Styling

### Backend (FastAPI)

#### API Routes

**Authentication (`/auth`)**
- `POST /register` - User registration
- `POST /login` - User login
- `GET /me` - Current user info

**Chat (`/chat`)**
- `POST /` - Send message
- `GET /history` - Get chat history

**Upload (`/upload`)**
- `POST /pdf` - Upload PDF
- `POST /query` - Query with RAG

**Metrics (`/metrics`)**
- `GET /summary` - Overall metrics
- `GET /usage` - Usage trends
- `GET /models` - Model performance
- `GET /evaluation` - Evaluation metrics

**Feedback (`/feedback`)**
- `POST /` - Submit feedback
- `GET /` - Get feedback

**Alerts (`/alerts`)**
- `GET /` - Get alerts
- `PATCH /{id}/resolve` - Resolve alert

**Agent (`/agent`)**
- `POST /analyze` - Agent analysis

#### Services

**Groq Service**
- LLM completion generation
- Token counting
- Cost calculation
- Error handling

**RAG Service**
- PDF processing
- Text chunking
- Document storage
- Context retrieval

**ChromaDB Service**
- Vector storage
- Semantic search
- Document management

**Security Checker**
- Prompt injection detection
- Input sanitization
- Security validation

#### Models (SQLAlchemy)

```
users
├── id (PK)
├── email
├── username
├── hashed_password
├── role
└── created_at

prompts
├── id (PK)
├── user_id (FK)
├── content
├── model
├── session_id
└── created_at

responses
├── id (PK)
├── prompt_id (FK)
├── user_id (FK)
├── content
├── tokens_used
├── latency_ms
├── cost
├── is_error
└── created_at

feedback
├── id (PK)
├── response_id (FK)
├── user_id (FK)
├── rating
└── comment

evaluations
├── id (PK)
├── response_id (FK)
├── faithfulness
├── relevance
├── ragas_score
└── created_at

alerts
├── id (PK)
├── type
├── severity
├── message
└── is_resolved

audit_logs
├── id (PK)
├── user_id (FK)
├── action
├── details
└── created_at
```

### LangGraph Agent

```
┌─────────────────┐
│ Analyze Request │
│  (Determine     │
│   Analysis Type)│
└────────┬────────┘
         │
    ┌────▼────┐
    │  Fetch  │
    │  Data   │
    └────┬────┘
         │
    ┌────▼────────┐
    │  Generate   │
    │  Insights   │
    │  (via Groq) │
    └────┬────────┘
         │
    ┌────▼────────┐
    │   Format    │
    │  Response   │
    └─────────────┘
```

### Data Flow

#### Chat Flow
```
User Input → Security Check → Sanitize → Save Prompt
                                              ↓
                                         Groq API
                                              ↓
                                      Save Response
                                              ↓
                                    Check for Alerts
                                              ↓
                                      Return to User
```

#### RAG Flow
```
PDF Upload → Extract Text → Chunk Text → Generate Embeddings
                                              ↓
                                        Store in ChromaDB
                                              
User Query → Retrieve Context → Enhance Prompt → Groq API
                                                      ↓
                                                Return Response
```

#### Monitoring Flow
```
Every Request → Log Prompt/Response → Track Metrics
                                            ↓
                                    Calculate Metrics
                                            ↓
                                    Update Database
                                            ↓
                                    Check Thresholds
                                            ↓
                                    Create Alerts
```

## Security Architecture

### Authentication Flow
```
Login Request → Verify Credentials → Generate JWT
                                          ↓
                                    Return Token
                                          
Protected Route → Extract Token → Verify Token → Get User
```

### Security Layers
1. **Input Validation** - Pydantic models
2. **Prompt Injection Detection** - Pattern matching
3. **Rate Limiting** - SlowAPI with Redis
4. **Authentication** - JWT tokens
5. **Authorization** - Role-based access
6. **Audit Logging** - All actions logged

## Scalability Considerations

### Horizontal Scaling
- Stateless backend (can run multiple instances)
- Session data in Redis
- Database connection pooling

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Cache frequently accessed data

### Database Optimization
- Indexes on frequently queried fields
- Query optimization
- Connection pooling
- Read replicas (future)

### Caching Strategy
- Redis for rate limiting
- In-memory caching for metrics
- CDN for frontend assets

## Monitoring & Observability

### Application Metrics
- Request count
- Latency distribution
- Error rates
- Token usage
- Cost tracking

### System Metrics
- CPU/Memory usage
- Database connections
- Queue lengths
- Response times

### Logging
- Structured logging
- Error tracking
- Audit trails
- Performance logs

## Technology Choices

### Why Next.js?
- Server-side rendering
- File-based routing
- Built-in optimizations
- Great developer experience

### Why FastAPI?
- High performance
- Automatic API docs
- Type hints
- Async support

### Why PostgreSQL?
- ACID compliance
- Rich query capabilities
- JSON support
- Mature ecosystem

### Why ChromaDB?
- Easy to use
- Built for embeddings
- Local persistence
- Python-friendly

### Why Groq?
- Fast inference
- Cost-effective
- Good model selection
- Easy API

## Future Enhancements

### Short Term
- [ ] Real-time dashboard updates
- [ ] Email notifications
- [ ] Data export functionality
- [ ] Advanced filtering

### Medium Term
- [ ] Multi-model comparison
- [ ] A/B testing support
- [ ] Custom evaluation metrics
- [ ] Team collaboration

### Long Term
- [ ] Multi-tenancy
- [ ] Advanced analytics
- [ ] ML-powered insights
- [ ] Custom model fine-tuning

## Performance Targets

- API response time: < 200ms (excluding LLM)
- LLM response time: < 3000ms
- Dashboard load time: < 2s
- Uptime: 99.9%
- Error rate: < 0.1%

## Deployment Architecture

### Development
```
localhost:3000 (Frontend) → localhost:8000 (Backend)
                                    ↓
                          localhost:5432 (PostgreSQL)
```

### Production
```
Vercel (Frontend) → Render (Backend) → Render PostgreSQL
                          ↓
                    Render Redis
```

## Security Checklist

- [x] JWT authentication
- [x] Password hashing
- [x] Input validation
- [x] Rate limiting
- [x] CORS configuration
- [x] Prompt injection detection
- [x] Audit logging
- [x] HTTPS (in production)
- [ ] API key rotation
- [ ] Security headers
- [ ] DDoS protection

## Cost Optimization

### Backend
- Use Groq (cost-effective)
- Implement caching
- Optimize queries
- Batch operations

### Frontend
- Static generation where possible
- Image optimization
- Code splitting
- CDN caching

### Database
- Index optimization
- Query optimization
- Connection pooling
- Data retention policies

## Testing Strategy

### Unit Tests
- Service layer tests
- Utility function tests
- Model validation tests

### Integration Tests
- API endpoint tests
- Database integration tests
- External API mocking

### E2E Tests
- User flow tests
- Critical path tests
- Cross-browser tests

### Performance Tests
- Load testing
- Stress testing
- Latency testing
