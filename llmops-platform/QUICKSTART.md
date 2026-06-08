# Quick Start Guide

Get the LLMOps Monitoring Platform running in 5 minutes!

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL (or use Docker)
- Groq API key ([Get one here](https://console.groq.com/))

## Step 1: Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd llmops-platform

# Copy environment files
cp .env.example .env
```

## Step 2: Start Database (Using Docker)

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Wait for services to be ready (about 10 seconds)
```

## Step 3: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Edit .env file and add your Groq API key
# GROQ_API_KEY=your-key-here

# Start backend
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000

## Step 4: Setup Frontend

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

Frontend will be available at: http://localhost:3000

## Step 5: Test the Application

1. Open http://localhost:3000 in your browser
2. Click "Create account"
3. Register with email, username, and password
4. You'll be redirected to the dashboard

## Quick Test

### Test Chat
1. Navigate to "Chat" page
2. Type a message: "What is machine learning?"
3. Click "Send"
4. View response with latency and cost metrics

### Test Dashboard
1. Navigate to "Dashboard"
2. View metrics including:
   - Total Requests
   - Average Latency
   - Token Usage
   - Cost Tracking

### Test RAG Upload
1. Navigate to "Upload" page
2. Upload a PDF document
3. Ask questions about the document

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## Common Issues

### Database Connection Error
```bash
# Make sure PostgreSQL is running
docker ps | grep postgres

# Check DATABASE_URL in .env file
```

### Port Already in Use
```bash
# Backend (8000)
# On Windows: netstat -ano | findstr :8000
# On Mac/Linux: lsof -ti:8000 | xargs kill -9

# Frontend (3000)
# On Windows: netstat -ano | findstr :3000
# On Mac/Linux: lsof -ti:3000 | xargs kill -9
```

### Missing Groq API Key
1. Get API key from https://console.groq.com/
2. Add to backend/.env: `GROQ_API_KEY=your-key-here`
3. Restart backend

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Explore API docs at http://localhost:8000/docs

## Using Docker Compose (All Services)

```bash
# Edit .env and add your API keys
cp .env.example .env

# Start all services
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Default Credentials

No default credentials. You must register a new account.

To make a user admin:
```sql
-- Connect to database
psql -h localhost -U llmops_user -d llmops_db

-- Update user role
UPDATE users SET role='admin' WHERE email='your@email.com';
```

## Support

- GitHub Issues: [Create an issue]
- Documentation: See README.md
- API Reference: http://localhost:8000/docs
