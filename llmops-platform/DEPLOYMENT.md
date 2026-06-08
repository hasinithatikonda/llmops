# Deployment Guide

This guide covers deploying the LLMOps Monitoring Platform to production.

## Table of Contents
1. [Backend Deployment (Render)](#backend-deployment-render)
2. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
3. [Database Setup (PostgreSQL)](#database-setup)
4. [Environment Variables](#environment-variables)
5. [CI/CD Setup](#cicd-setup)

## Backend Deployment (Render)

### Prerequisites
- GitHub account
- Render account (free tier available)
- Groq API key

### Steps

1. **Create PostgreSQL Database on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "PostgreSQL"
   - Name: `llmops-db`
   - Database: `llmops_db`
   - User: `llmops_user`
   - Region: Choose closest to your users
   - Plan: Free (or paid for production)
   - Click "Create Database"
   - Save the Internal Database URL

2. **Create Redis Instance**
   - Click "New +" → "Redis"
   - Name: `llmops-redis`
   - Plan: Free (or paid)
   - Click "Create Redis"
   - Save the Internal Redis URL

3. **Deploy Backend Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository
   - Configure:
     - **Name**: `llmops-backend`
     - **Region**: Same as database
     - **Branch**: `main`
     - **Root Directory**: `backend`
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   
4. **Set Environment Variables**
   - In the Environment tab, add:
     ```
     DATABASE_URL=<your-postgres-internal-url>
     REDIS_URL=<your-redis-internal-url>
     SECRET_KEY=<generate-random-secret>
     GROQ_API_KEY=<your-groq-api-key>
     LANGSMITH_API_KEY=<your-langsmith-api-key>
     FRONTEND_URL=<your-vercel-url>
     ENVIRONMENT=production
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     CHROMA_PERSIST_DIR=/opt/render/project/chroma_db
     ```

5. **Generate Secret Key**
   ```python
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Save the service URL (e.g., `https://llmops-backend.onrender.com`)

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (free tier available)
- Backend URL from Render

### Option 1: Using Vercel Dashboard

1. **Import Project**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Select the repository

2. **Configure Project**
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

3. **Set Environment Variables**
   - Add environment variable:
     ```
     NEXT_PUBLIC_API_URL=https://llmops-backend.onrender.com
     ```

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment
   - Save the deployment URL

### Option 2: Using Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from Frontend Directory**
   ```bash
   cd frontend
   vercel
   ```

4. **Set Environment Variable**
   ```bash
   vercel env add NEXT_PUBLIC_API_URL production
   # Enter: https://llmops-backend.onrender.com
   ```

5. **Deploy to Production**
   ```bash
   vercel --prod
   ```

## Database Setup

### Automatic Migration
The backend automatically creates tables on startup. No manual migration needed.

### Manual Migration (if needed)
```python
from app.core.database import Base, engine
Base.metadata.create_all(bind=engine)
```

### Create Admin User
After deployment, create an admin user:

```bash
# Using Render Shell
curl -X POST https://llmops-backend.onrender.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "username": "admin",
    "password": "SecurePassword123!"
  }'

# Then update role to admin in database
```

## Environment Variables

### Backend Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| DATABASE_URL | PostgreSQL connection string | Yes | `postgresql://user:pass@host/db` |
| SECRET_KEY | JWT secret key | Yes | `random-secret-key` |
| GROQ_API_KEY | Groq API key | Yes | `gsk_...` |
| LANGSMITH_API_KEY | LangSmith API key | No | `ls__...` |
| REDIS_URL | Redis connection string | Yes | `redis://host:6379` |
| FRONTEND_URL | Frontend URL for CORS | Yes | `https://your-app.vercel.app` |
| ENVIRONMENT | Environment name | Yes | `production` |
| CHROMA_PERSIST_DIR | ChromaDB directory | Yes | `/opt/render/project/chroma_db` |

### Frontend Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| NEXT_PUBLIC_API_URL | Backend API URL | Yes | `https://api.example.com` |

## CI/CD Setup

### GitHub Actions Setup

1. **Add GitHub Secrets**
   - Go to repository Settings → Secrets and variables → Actions
   - Add secrets:
     - `RENDER_SERVICE_ID`: From Render service settings
     - `RENDER_API_KEY`: From Render account settings
     - `VERCEL_TOKEN`: From Vercel account settings
     - `VERCEL_ORG_ID`: From Vercel project settings
     - `VERCEL_PROJECT_ID`: From Vercel project settings

2. **Workflow File**
   - Already created at `.github/workflows/deploy.yml`
   - Automatically deploys on push to main branch

3. **Manual Deployment**
   - Go to Actions tab
   - Select "Deploy to Production"
   - Click "Run workflow"

## Post-Deployment Checklist

- [ ] Backend is accessible at the Render URL
- [ ] Frontend is accessible at the Vercel URL
- [ ] Database connection is working
- [ ] Redis connection is working
- [ ] API endpoints return expected responses
- [ ] Authentication is working
- [ ] Chat functionality is working
- [ ] PDF upload is working
- [ ] Dashboard shows metrics
- [ ] CORS is properly configured
- [ ] Environment variables are set
- [ ] HTTPS is enabled (automatic on Render/Vercel)
- [ ] Create first admin user
- [ ] Test all features

## Testing Deployment

### Test Backend Health
```bash
curl https://llmops-backend.onrender.com/health
```

### Test Authentication
```bash
curl -X POST https://llmops-backend.onrender.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPassword123!"
  }'
```

### Test Chat
```bash
curl -X POST https://llmops-backend.onrender.com/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "message": "Hello, how are you?",
    "model": "mixtral-8x7b-32768"
  }'
```

## Monitoring

### Render Logs
- View logs in Render dashboard
- Enable log persistence for debugging

### Vercel Logs
- View deployment logs in Vercel dashboard
- Monitor function invocations

### Application Monitoring
- Use the built-in alerts system
- Monitor latency and error rates
- Track token usage and costs

## Scaling

### Backend Scaling (Render)
- Upgrade to paid plan for:
  - More CPU/RAM
  - Auto-scaling
  - Better performance
  - No cold starts

### Database Scaling
- Upgrade PostgreSQL plan for:
  - More storage
  - Better performance
  - Connection pooling
  - Backups

### Frontend Scaling
- Vercel automatically scales
- No manual configuration needed

## Troubleshooting

### Backend Not Starting
1. Check environment variables
2. Check database connection
3. View logs in Render dashboard
4. Verify Groq API key is valid

### Frontend Not Connecting to Backend
1. Verify NEXT_PUBLIC_API_URL is correct
2. Check CORS settings in backend
3. Verify backend is running
4. Check browser console for errors

### Database Connection Issues
1. Verify DATABASE_URL is correct
2. Check if database is running
3. Verify network access
4. Check PostgreSQL logs

### ChromaDB Issues
1. Verify CHROMA_PERSIST_DIR path
2. Check disk space
3. Clear ChromaDB if corrupted
4. Restart backend service

## Security Recommendations

1. **Use Strong Secrets**
   - Generate random SECRET_KEY
   - Use different keys for dev/prod

2. **Enable HTTPS**
   - Automatic on Render/Vercel
   - Enforce HTTPS in production

3. **Secure API Keys**
   - Never commit API keys
   - Use environment variables
   - Rotate keys regularly

4. **Rate Limiting**
   - Already configured with SlowAPI
   - Adjust limits based on usage

5. **Database Security**
   - Use strong passwords
   - Enable SSL connections
   - Regular backups

6. **Monitor Access**
   - Review audit logs
   - Monitor unusual activity
   - Set up alerts

## Backup Strategy

### Database Backups
- Render provides automatic backups
- Export data regularly
- Test restore procedures

### ChromaDB Backups
- Implement periodic backups
- Store in cloud storage (S3, etc.)

## Cost Estimation

### Free Tier Limits
- **Render**: 750 hours/month, 512MB RAM
- **Vercel**: 100GB bandwidth, unlimited requests
- **PostgreSQL**: Limited storage
- **Redis**: Limited memory

### Paid Plans
- **Render**: $7-25/month per service
- **Vercel**: $20/month for Pro
- **PostgreSQL**: $7+/month
- **Redis**: $5+/month

## Support

For deployment issues:
1. Check logs first
2. Review this guide
3. Check README.md
4. Open GitHub issue
5. Contact support

## Additional Resources

- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
