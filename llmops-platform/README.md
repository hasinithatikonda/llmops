# LLMOps Monitoring Platform

A production-ready LLMOps monitoring and evaluation platform built with Next.js, FastAPI, and Groq API. Monitor your LLM applications with real-time analytics, RAG capabilities, and comprehensive metrics tracking.

## 🚀 Live Deployment

- **Backend API**: https://llmopsbackend.onrender.com
- **API Documentation**: https://llmopsbackend.onrender.com/docs
- **Health Check**: https://llmopsbackend.onrender.com/health
- **Frontend**: Deployed on Vercel
- **Repository**: https://github.com/hasinithatikonda/llmops

## ✨ Key Features

### 🔐 Authentication & Security
- JWT-based authentication with secure token management
- Role-based access control (Admin/User)
- Password hashing with bcrypt
- CORS protection
- Input validation and sanitization

### 💬 Multi-Model Chat
- Support for multiple Groq models:
  - **Llama 3.3 70B Versatile** - Most capable, best for complex tasks
  - **Llama 3.1 8B Instant** - Ultra-fast responses
  - **Llama 4 Scout 17B** - Optimized for instruction following
- Real-time chat interface
- Session management
- Conversation history

### 📊 Advanced Analytics
- **Real-time Metrics Dashboard**
  - Total requests and active users
  - Token usage and cost tracking
  - Average latency monitoring
  - Error rate analytics
- **Model-specific Performance**
  - Per-model token consumption
  - Response time comparison
  - Cost analysis per model
- **Interactive Charts**
  - Usage trends over time
  - Token consumption patterns
  - Cost breakdowns

### 📚 RAG (Retrieval-Augmented Generation)
- PDF document upload and processing
- Automatic document chunking and indexing
- Vector storage with ChromaDB
- Semantic search and retrieval
- Context-aware responses
- Multi-document support
- Model selection for RAG queries

### 📈 Monitoring & Evaluation
- Token usage tracking (input + output)
- Response latency measurement
- Cost calculation per request
- Error logging and tracking
- User feedback collection
- Model performance comparison

## 🏗️ Tech Stack

### Backend
- **Framework**: FastAPI 0.115.0
- **Language**: Python 3.11
- **Database**: In-Memory (Development) / PostgreSQL (Production Ready)
- **Vector DB**: ChromaDB 0.4.22
- **LLM Provider**: Groq API
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt 4.0.1
- **Validation**: Pydantic 2.9.2
- **HTTP Client**: httpx 0.27.2
- **Deployment**: Render

### Frontend
- **Framework**: Next.js 16.2.7 (React 19)
- **Language**: TypeScript 5.3.3
- **Styling**: Tailwind CSS 3.4.1
- **Charts**: Recharts 2.10.3
- **HTTP Client**: Axios 1.6.5
- **Icons**: Lucide React 0.460.0
- **Date Handling**: date-fns 3.2.0
- **Deployment**: Vercel

## 📋 Prerequisites

### Required
- Python 3.11 or higher
- Node.js 20 or higher
- Groq API key (get one at https://console.groq.com)

### Optional (for production)
- PostgreSQL 15+ (for persistent storage)
- Redis (for rate limiting)
- MongoDB (alternative storage option)

## 🚀 Quick Start - Using Deployed Version

### 1. Access the Application

Visit your deployed frontend URL or the backend API directly:
- **API Docs**: https://llmopsbackend.onrender.com/docs
- **Health Check**: https://llmopsbackend.onrender.com/health

### 2. Login or Register

**Option A: Use Pre-configured Test Account**
- Email: `test@example.com`
- Password: `password123`

**Option B: Register New Account**
1. Go to `/register` page
2. Enter email, username, and password (8+ characters)
3. Click "Create account"
4. You'll be automatically logged in

**Note**: The backend uses in-memory storage by default, so user data is reset on each deployment. Use the pre-configured account for consistent access.

### 3. Explore Features

**💬 Chat with AI Models**
1. Navigate to Chat page
2. Select your preferred model from dropdown
3. Type your message
4. Get instant AI-powered responses

**📚 Upload and Query Documents (RAG)**
1. Go to Upload/RAG page
2. Upload a PDF document
3. Wait for processing (chunking and indexing)
4. Ask questions about the document
5. Select model for query processing
6. Get context-aware answers

**📊 View Analytics Dashboard**
1. Navigate to Dashboard
2. View real-time metrics:
   - Total API requests
   - Token usage and costs
   - Average response latency
   - Active users
3. Analyze model-specific performance
4. Track usage trends over time

## 💻 Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/hasinithatikonda/llmops.git
cd llmops/llmops-platform
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_groq_api_key_here
```

**Edit `backend/.env`:**
```env
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GROQ_API_KEY=your_groq_api_key_here
FRONTEND_URL=http://localhost:3000
```

**Run the backend:**
```bash
# Using main_simple.py (in-memory storage, no database required)
uvicorn app.main_simple:app --reload --port 8000

# Backend will run on http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Edit .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Run the frontend:**
```bash
npm run dev

# Frontend will run on http://localhost:3000
```

### 4. Access Local Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

## 🐳 Docker Deployment (Optional)

### Using Docker Compose

```bash
# Create .env file with your Groq API key
cp .env.example .env

# Build and start services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

## 🌐 Production Deployment

### Backend - Render

**Prerequisites:**
- Render account
- GitHub repository

**Steps:**

1. **Create Web Service on Render**
   - Go to https://dashboard.render.com/
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the `llmops` repository

2. **Configure Service**
   - **Name**: `llmops-backend`
   - **Root Directory**: `llmops-platform/backend`
   - **Environment**: Python 3
   - **Python Version**: 3.11.11 (create `runtime.txt` with this)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main_simple:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables**
   ```
   SECRET_KEY=<generate-random-string>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   GROQ_API_KEY=<your-groq-api-key>
   FRONTEND_URL=<your-vercel-url>
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - Note your backend URL: `https://your-service.onrender.com`

### Frontend - Vercel

**Prerequisites:**
- Vercel account
- GitHub repository

**Steps:**

1. **Import Project**
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Select the `llmops` repository

2. **Configure Project**
   - **Root Directory**: `llmops-platform/frontend`
   - **Framework Preset**: Next.js (auto-detected)
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

3. **Add Environment Variable**
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://your-render-backend-url.onrender.com`
   - **Environments**: Production, Preview, Development

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment (1-2 minutes)
   - Access your frontend at the provided URL

### Post-Deployment Configuration

1. **Update CORS in Backend**
   - Add your Vercel frontend URL to CORS allowed origins
   - Already configured to allow all Vercel deployments: `https://*.vercel.app`

2. **Test Deployment**
   - Visit your frontend URL
   - Register or login with test account
   - Try chat feature
   - Upload a PDF and test RAG
   - Check dashboard metrics

## 📚 API Documentation

### Authentication Endpoints

```
POST /auth/register
Body: { "email": "user@example.com", "username": "user", "password": "password123" }
Response: { "access_token": "...", "token_type": "bearer", "user": {...} }

POST /auth/login  
Body: { "email": "user@example.com", "password": "password123" }
Response: { "access_token": "...", "token_type": "bearer", "user": {...} }

GET /auth/me
Headers: { "Authorization": "Bearer <token>" }
Response: { "id": 1, "email": "...", "username": "...", "role": "user" }
```

### Chat Endpoints

```
POST /chat
Headers: { "Authorization": "Bearer <token>" }
Body: { "message": "Hello", "model": "llama-3.3-70b-versatile", "session_id": "..." }
Response: { "response": "...", "session_id": "...", "model": "...", "tokens_used": 100, "latency_ms": 250 }

GET /chat/history
Headers: { "Authorization": "Bearer <token>" }
Response: [ {...}, {...} ]
```

### Upload & RAG Endpoints

```
POST /upload/pdf
Headers: { "Authorization": "Bearer <token>", "Content-Type": "multipart/form-data" }
Body: FormData with 'file' field
Response: { "filename": "...", "pages": 10, "chunks": 50 }

POST /upload/query
Headers: { "Authorization": "Bearer <token>" }
Body: { "query": "What is...", "model": "llama-3.3-70b-versatile" }
Response: { "answer": "...", "model": "...", "tokens_used": 150 }
```

### Metrics Endpoints

```
GET /metrics/summary
Headers: { "Authorization": "Bearer <token>" }
Response: { "total_requests": 100, "active_users": 5, "total_tokens": 50000, "total_cost": 0.01 }

GET /metrics/models
Headers: { "Authorization": "Bearer <token>" }
Response: [ { "model": "llama-3.3-70b-versatile", "usage_count": 50, "total_tokens": 25000, "avg_latency": 300 } ]

GET /metrics/rag
Headers: { "Authorization": "Bearer <token>" }
Response: { "total_uploads": 5, "total_queries": 20, "total_tokens": 15000 }
```

### Health Check

```
GET /health
Response: { "status": "healthy", "timestamp": "2026-06-09T..." }
```

## 🔧 Configuration

### Backend Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | JWT secret key | - | Yes |
| `ALGORITHM` | JWT algorithm | HS256 | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time | 30 | No |
| `GROQ_API_KEY` | Groq API key | - | Yes |
| `FRONTEND_URL` | Frontend URL for CORS | http://localhost:3000 | Yes |
| `DATABASE_URL` | PostgreSQL URL (optional) | - | No |
| `MONGODB_URI` | MongoDB URL (optional) | - | No |
| `REDIS_URL` | Redis URL (optional) | - | No |

### Frontend Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | http://localhost:8000 | Yes |

## 🗄️ Database Schema

### Users
```sql
- id: INTEGER (Primary Key)
- email: STRING (Unique)
- username: STRING
- password: STRING (Hashed with bcrypt)
- role: STRING (user/admin)
- is_active: BOOLEAN
- created_at: DATETIME
```

### Activity Tracking (In-Memory)
```python
{
  "user_id": {
    "total_requests": int,
    "total_tokens": int,
    "total_cost": float,
    "model_usage": {
      "model_name": {
        "requests": int,
        "tokens": int,
        "errors": int,
        "total_latency": float
      }
    },
    "rag_metrics": {
      "uploads": int,
      "queries": int,
      "total_tokens": int
    }
  }
}
```

## 🛡️ Security Features

1. **Authentication**
   - JWT tokens with expiration
   - Secure token generation
   - Bearer token authentication

2. **Password Security**
   - bcrypt hashing with salt
   - Minimum 8 characters requirement
   - Secure password verification

3. **CORS Protection**
   - Configured allowed origins
   - Wildcard support for Vercel deployments
   - Custom middleware for preflight requests

4. **Input Validation**
   - Pydantic models for request validation
   - Email validation
   - Type checking

5. **API Security**
   - Protected endpoints require authentication
   - User-specific data isolation
   - Error message sanitization

## 🐛 Troubleshooting

### Common Issues

**1. "Invalid API Key" Error**
- **Cause**: Groq API key not set or incorrect
- **Solution**: 
  - Check Render Environment variables
  - Verify API key is correct
  - Look for `✓ Groq API key loaded (length: 59 chars)` in logs

**2. Login Fails After Deployment**
- **Cause**: In-memory storage resets on deployment
- **Solution**: 
  - Use pre-configured account: `test@example.com` / `password123`
  - Or register a new account on the deployed site

**3. CORS Errors**
- **Cause**: Frontend URL not in allowed origins
- **Solution**: 
  - Check `FRONTEND_URL` environment variable in Render
  - Verify CORS middleware is configured correctly
  - Already configured to allow `*.vercel.app`

**4. Chat Returns 500 Error**
- **Cause**: Groq API issue or model unavailable
- **Solution**:
  - Check Render logs for detailed error
  - Verify Groq API key is valid
  - Try different model
  - Check Groq API status

**5. PDF Upload Fails**
- **Cause**: File size too large or ChromaDB issue
- **Solution**:
  - Keep PDFs under 10MB
  - Check ChromaDB initialization in logs
  - Verify sufficient disk space on Render

### Debug Mode

Enable detailed logging:

```python
# In main_simple.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Logs

**Render:**
- Dashboard → Your Service → Logs tab
- Look for error messages and stack traces

**Local:**
```bash
# Backend logs appear in terminal
# Check for errors, warnings, and debug messages
```

## 📊 Monitoring & Analytics

### Metrics Tracked

- **Request Metrics**
  - Total API requests
  - Requests per user
  - Requests per model

- **Token Usage**
  - Total tokens consumed
  - Input vs output tokens
  - Tokens per model
  - Tokens per user

- **Performance Metrics**
  - Average response latency
  - Latency per model
  - Error rates
  - Success rates

- **Cost Tracking**
  - Total estimated cost
  - Cost per model
  - Cost per user
  - Cost trends

### Available Models

| Model | Description | Max Tokens | Speed |
|-------|-------------|------------|-------|
| llama-3.3-70b-versatile | Most capable, best for complex reasoning | 6000 | Medium |
| llama-3.1-8b-instant | Ultra-fast, great for simple queries | 2000 | Very Fast |
| meta-llama/llama-4-scout-17b-16e-instruct | Optimized for instructions | 6000 | Fast |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Groq** - For lightning-fast LLM inference
- **FastAPI** - For the excellent backend framework
- **Next.js** - For the powerful React framework
- **Vercel** - For seamless frontend deployment
- **Render** - For reliable backend hosting
- **ChromaDB** - For vector storage capabilities

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## 🗺️ Roadmap

- [ ] PostgreSQL integration for persistent storage
- [ ] MongoDB support as alternative storage
- [ ] Advanced RAG techniques (hybrid search, reranking)
- [ ] Real-time chat with WebSockets
- [ ] Multi-user chat rooms
- [ ] Export metrics to CSV/JSON
- [ ] Email notifications for errors
- [ ] Advanced user roles and permissions
- [ ] API rate limiting with Redis
- [ ] LangSmith integration for evaluation
- [ ] RAGAS metrics for RAG quality
- [ ] A/B testing for models
- [ ] Custom evaluation metrics
- [ ] Prompt templates library
- [ ] Batch processing for documents

---

**Built with ❤️ for the LLMOps community**

**Last Updated:** June 9, 2026
