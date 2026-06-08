# LLMOps Platform Architecture with MongoDB

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE                            │
│                     (Browser - localhost:3000)                      │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ HTTP/REST API
                             │ (Authorization: Bearer Token)
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                        FASTAPI BACKEND                              │
│                    (Python - localhost:8000)                        │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  API Endpoints                                                │ │
│  │  • POST /auth/login, /auth/register                          │ │
│  │  • POST /chat (save to MongoDB)                              │ │
│  │  • GET /conversations (fetch from MongoDB)                   │ │
│  │  • GET /conversations/{id}/messages                          │ │
│  │  • DELETE /conversations/{id}                                │ │
│  │  • GET /metrics/summary, /usage, /models                     │ │
│  └───────────────────────────┬───────────────────────────────────┘ │
│                              │                                      │
│  ┌───────────────────────────▼───────────────────────────────────┐ │
│  │  Business Logic Layer                                         │ │
│  │  • User Authentication (JWT)                                  │ │
│  │  • Chat Message Processing                                    │ │
│  │  • Conversation Management                                    │ │
│  │  • Metrics Aggregation                                        │ │
│  └───────────┬───────────────────────────────────┬───────────────┘ │
└──────────────┼───────────────────────────────────┼─────────────────┘
               │                                   │
               │                                   │
       ┌───────▼────────┐                 ┌────────▼─────────┐
       │  GROQ API      │                 │    MONGODB       │
       │  (groq.com)    │                 │   DATABASE       │
       │                │                 │                  │
       │ • LLM Models:  │                 │ Collections:     │
       │   - Llama 3.3  │                 │ • users          │
       │   - Llama 3.1  │                 │ • conversations  │
       │   - Llama 4    │                 │ • chat_messages  │
       │                │                 │ • user_activity  │
       │ • Inference    │                 │                  │
       │ • Tokenization │                 │ Location:        │
       └────────────────┘                 │ • Atlas (Cloud)  │
                                          │   OR             │
                                          │ • localhost:27017│
                                          └──────────────────┘
```

## Data Flow

### 1. User Authentication Flow
```
User (Browser)
    │
    ├─→ POST /auth/login
    │   { email, password }
    │
    ├─→ FastAPI Backend
    │   ├─→ Query MongoDB users collection
    │   ├─→ Verify password (bcrypt)
    │   └─→ Generate JWT token
    │
    └─→ Response
        { access_token, user_info }
```

### 2. Chat Message Flow
```
User Types Message
    │
    ├─→ POST /chat
    │   { message, conversation_id?, model }
    │   Authorization: Bearer <token>
    │
    ├─→ FastAPI Backend
    │   │
    │   ├─→ 1. Verify JWT token → Get user_id
    │   │
    │   ├─→ 2. Get/Create Conversation
    │   │      MongoDB.conversations.insert_one()
    │   │      → conversation_id
    │   │
    │   ├─→ 3. Save User Message
    │   │      MongoDB.chat_messages.insert_one({
    │   │        conversation_id,
    │   │        role: "user",
    │   │        content: message
    │   │      })
    │   │
    │   ├─→ 4. Call Groq API
    │   │      groq_client.chat.completions.create()
    │   │      ├─→ Send user message
    │   │      └─→ Get AI response
    │   │
    │   ├─→ 5. Save AI Response
    │   │      MongoDB.chat_messages.insert_one({
    │   │        conversation_id,
    │   │        role: "assistant",
    │   │        content: response,
    │   │        model, tokens_used, latency_ms, cost
    │   │      })
    │   │
    │   ├─→ 6. Update Conversation
    │   │      MongoDB.conversations.update_one({
    │   │        updated_at: now(),
    │   │        message_count: +2
    │   │      })
    │   │
    │   └─→ 7. Update User Activity
    │          MongoDB.user_activity.update_one({
    │            total_tokens: +tokens,
    │            total_cost: +cost,
    │            model_usage[model]: +stats
    │          })
    │
    └─→ Response
        {
          response: "AI message",
          conversation_id,
          message_id,
          tokens_used,
          latency_ms
        }
```

### 3. Fetch Conversations Flow
```
User Opens Chat Page
    │
    ├─→ GET /conversations
    │   Authorization: Bearer <token>
    │
    ├─→ FastAPI Backend
    │   ├─→ Verify JWT → Get user_id
    │   ├─→ MongoDB.conversations.find({ user_id })
    │   │      .sort({ updated_at: -1 })
    │   │      .limit(50)
    │   └─→ Return conversation list
    │
    └─→ Response
        [
          { id, title, created_at, updated_at, message_count },
          ...
        ]
```

### 4. Get Messages in Conversation Flow
```
User Clicks Conversation
    │
    ├─→ GET /conversations/{conv_id}/messages
    │   Authorization: Bearer <token>
    │
    ├─→ FastAPI Backend
    │   ├─→ Verify JWT → Get user_id
    │   ├─→ Verify conversation ownership
    │   ├─→ MongoDB.chat_messages.find({ 
    │   │      conversation_id: conv_id
    │   │   }).sort({ timestamp: 1 })
    │   └─→ Return all messages
    │
    └─→ Response
        [
          { id, role: "user", content, timestamp },
          { id, role: "assistant", content, model, tokens, ... },
          ...
        ]
```

### 5. Metrics Dashboard Flow
```
User Views Dashboard
    │
    ├─→ GET /metrics/summary?model=llama-3.3-70b-versatile
    │   Authorization: Bearer <token>
    │
    ├─→ FastAPI Backend
    │   ├─→ Verify JWT → Get user_id
    │   ├─→ MongoDB.user_activity.findOne({ user_id })
    │   ├─→ Calculate aggregations:
    │   │   • Total requests
    │   │   • Active models count
    │   │   • Average latency
    │   │   • Total tokens & cost
    │   │   • Get max_tokens for selected model
    │   └─→ Return metrics
    │
    └─→ Response
        {
          total_requests: 247,
          active_models: 3,
          average_latency: 1250.5,
          total_tokens: 125840,
          total_cost: 0.0302,
          max_tokens: 6000
        }
```

## MongoDB Schema Design

### Collection Relationships

```
users (1)
  │
  │ user_id
  │
  ├─→ conversations (N)
  │     │
  │     │ conversation_id
  │     │
  │     └─→ chat_messages (N)
  │           • role: user/assistant
  │           • content
  │           • model, tokens, etc.
  │
  └─→ user_activity (1)
        • Aggregated stats
        • Per-date breakdown
        • Per-model breakdown
```

### Indexes for Performance

```javascript
// users collection
users.createIndex({ email: 1 }, { unique: true })
users.createIndex({ username: 1 })

// conversations collection
conversations.createIndex({ user_id: 1 })
conversations.createIndex({ created_at: -1 })
conversations.createIndex({ user_id: 1, created_at: -1 })

// chat_messages collection
chat_messages.createIndex({ user_id: 1 })
chat_messages.createIndex({ conversation_id: 1 })
chat_messages.createIndex({ timestamp: -1 })
chat_messages.createIndex({ user_id: 1, timestamp: -1 })

// user_activity collection
user_activity.createIndex({ user_id: 1 }, { unique: true })
user_activity.createIndex({ last_activity: -1 })
```

## Technology Stack

### Frontend
- **Framework**: Next.js 14 (React 18)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **State**: React Hooks (useState, useEffect)
- **Storage**: LocalStorage (cache) + API (source of truth)

### Backend
- **Framework**: FastAPI 0.109.0
- **Language**: Python 3.14
- **Auth**: JWT (python-jose)
- **Password**: bcrypt (passlib)
- **Database Driver**: 
  - Motor 3.3.2 (async)
  - PyMongo 4.6.1 (sync)
- **CORS**: fastapi.middleware.cors

### Database
- **Primary**: MongoDB
  - Atlas (Cloud) OR
  - Community Server (Local)
- **Collections**: 6 (users, conversations, chat_messages, user_activity, metrics, evaluations)
- **Indexes**: Optimized for queries

### AI/LLM
- **Provider**: Groq
- **Models**: 
  - llama-3.3-70b-versatile (6K tokens)
  - llama-3.1-8b-instant (2K tokens)
  - llama-4-scout-17b-16e-instruct (6K tokens)
- **API**: Groq Python SDK

## Deployment Architecture

### Development
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Frontend   │────▶│   Backend   │────▶│   MongoDB   │
│ localhost:  │     │ localhost:  │     │ localhost:  │
│    3000     │     │    8000     │     │   27017     │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Production (Example)
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Vercel     │────▶│    Render    │────▶│    Atlas     │
│   (Next.js)  │     │   (FastAPI)  │     │  (MongoDB)   │
│              │     │              │     │              │
│ https://     │     │ https://     │     │ https://     │
│ app.com      │     │ api.app.com  │     │ cloud.mongo  │
└──────────────┘     └──────────────┘     └──────────────┘
```

## Security Layers

```
┌─────────────────────────────────────────────────────┐
│  1. Network Layer                                   │
│     • HTTPS/TLS encryption                          │
│     • CORS policy                                   │
│     • IP whitelisting (MongoDB Atlas)               │
└─────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│  2. Application Layer                               │
│     • JWT token authentication                      │
│     • Password hashing (bcrypt)                     │
│     • User session management                       │
└─────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│  3. Database Layer                                  │
│     • User-based access control                     │
│     • Query parameterization                        │
│     • Encryption at rest (Atlas)                    │
└─────────────────────────────────────────────────────┘
```

## Scalability Considerations

### Horizontal Scaling
- **Frontend**: Static files → CDN
- **Backend**: Multiple FastAPI instances → Load balancer
- **Database**: MongoDB sharding → Distributed data

### Vertical Scaling
- **Frontend**: Larger server instance
- **Backend**: More CPU/RAM for FastAPI
- **Database**: Upgrade MongoDB tier (Atlas)

### Caching Strategy
- **Frontend**: LocalStorage for UI state
- **Backend**: Redis for session cache (future)
- **Database**: MongoDB query cache (automatic)

## Performance Optimizations

### Database
- ✅ Indexes on frequently queried fields
- ✅ Compound indexes for common queries
- ✅ Array slicing ($slice) for large arrays
- ✅ Projection to limit returned fields

### Backend
- ✅ Async/await for I/O operations
- ✅ Connection pooling (Motor)
- ✅ Minimal data processing
- ✅ Efficient aggregation pipelines

### Frontend
- ✅ Lazy loading conversations
- ✅ Pagination for large lists
- ✅ Debounced search inputs
- ✅ Optimistic UI updates

## Monitoring & Observability

### Application Metrics
- Request count
- Response times
- Error rates
- Token usage
- Cost tracking

### Database Metrics (Atlas)
- Connection count
- Query performance
- Storage usage
- Index efficiency
- Slow queries

### Business Metrics
- Active users
- Chat frequency
- Model usage distribution
- Average session duration
- Token consumption by model

## Disaster Recovery

### Backup Strategy
- **Atlas**: Automatic continuous backups
- **Local**: Manual mongodump schedules
- **Retention**: Point-in-time recovery

### Recovery Process
1. Identify failure point
2. Restore from backup
3. Verify data integrity
4. Resume operations

## Future Enhancements

### Phase 1: Enhanced Features
- [ ] Real-time sync (WebSockets)
- [ ] Conversation search
- [ ] Message reactions
- [ ] Conversation sharing

### Phase 2: Advanced Analytics
- [ ] Custom dashboards
- [ ] Export reports
- [ ] Cost optimization insights
- [ ] Model comparison tools

### Phase 3: Enterprise Features
- [ ] Team workspaces
- [ ] Role-based permissions
- [ ] Audit logging
- [ ] SSO integration
- [ ] API rate limiting

---

**This architecture provides a solid foundation for a production-ready LLMOps monitoring platform!** 🚀
