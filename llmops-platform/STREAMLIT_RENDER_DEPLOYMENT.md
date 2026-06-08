# 🚀 Streamlit + Render Deployment Guide

Complete guide to deploy your LLMOps Platform using Streamlit (frontend) and Render (hosting).

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Local Testing](#local-testing)
5. [Deploy Backend to Render](#deploy-backend-to-render)
6. [Deploy Frontend to Render](#deploy-frontend-to-render)
7. [Configure Environment Variables](#configure-environment-variables)
8. [Testing Deployment](#testing-deployment)
9. [Troubleshooting](#troubleshooting)

---

## 📖 Overview

This deployment uses:
- **Backend**: FastAPI hosted on Render
- **Frontend**: Streamlit app hosted on Render
- **Database**: In-memory storage (can be upgraded to MongoDB)
- **LLM API**: Groq API for AI responses

**Cost**: FREE tier available on Render!

---

## 🏗️ Architecture

```
┌─────────────────┐
│   User Browser  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Streamlit Frontend     │
│  (Render Web Service)   │
│  Port: 8501             │
└────────┬────────────────┘
         │
         │ HTTP Requests
         ▼
┌─────────────────────────┐
│  FastAPI Backend        │
│  (Render Web Service)   │
│  Port: 8000             │
└────────┬────────────────┘
         │
         ▼
    ┌─────────┐
    │ Groq API│
    └─────────┘
```

---

## ✅ Prerequisites

1. **GitHub Account** ✓ (You already have the repo)
2. **Render Account** (Free): https://render.com
3. **Groq API Key**: https://console.groq.com/keys

---

## 🧪 Local Testing

Before deploying, test the Streamlit app locally:

### 1. Start Backend (Terminal 1)
```bash
cd c:\Users\hasin\OneDrive\Documents\llmops\llmops-platform\backend
venv\Scripts\activate
python app/main_simple.py
```

Backend runs on: http://localhost:8000

### 2. Start Streamlit Frontend (Terminal 2)
```bash
cd c:\Users\hasin\OneDrive\Documents\llmops\llmops-platform\streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

Frontend runs on: http://localhost:8501

### 3. Test Login
- Email: `test@example.com`
- Password: `password123`

---

## 🚀 Deploy Backend to Render

### Step 1: Create New Web Service

1. Go to https://render.com and sign in
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repository: `hasinithatikonda/llmops`

### Step 2: Configure Backend Service

**Basic Settings:**
- **Name**: `llmops-backend`
- **Region**: `Oregon (US West)` (or closest to you)
- **Branch**: `main`
- **Root Directory**: `llmops-platform/backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main_simple:app --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | (Generate random string, e.g., `your-super-secret-key-12345`) |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `GROQ_API_KEY` | `gsk_your_groq_api_key_here` |
| `FRONTEND_URL` | `https://llmops-frontend.onrender.com` (update after frontend deployment) |

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Note your backend URL: `https://llmops-backend.onrender.com`

---

## 🎨 Deploy Frontend to Render

### Step 1: Create Another Web Service

1. Click **"New"** → **"Web Service"**
2. Connect same GitHub repository

### Step 2: Configure Frontend Service

**Basic Settings:**
- **Name**: `llmops-frontend`
- **Region**: `Oregon (US West)` (same as backend)
- **Branch**: `main`
- **Root Directory**: `llmops-platform/streamlit_app`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

### Step 3: Add Environment Variables

| Key | Value |
|-----|-------|
| `API_URL` | `https://llmops-backend.onrender.com` (your backend URL from Step 1) |

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Your frontend URL: `https://llmops-frontend.onrender.com`

---

## ⚙️ Configure Environment Variables

### Update Backend FRONTEND_URL

1. Go to your backend service on Render
2. Click **"Environment"**
3. Update `FRONTEND_URL` to: `https://llmops-frontend.onrender.com`
4. Save and redeploy

### Add Groq API Key

1. Go to https://console.groq.com/keys
2. Create new API key
3. Copy the key
4. In Render backend service → Environment → Add `GROQ_API_KEY`
5. Save and redeploy

---

## ✅ Testing Deployment

### 1. Access Frontend
Visit: `https://llmops-frontend.onrender.com`

### 2. Test Login
- Email: `test@example.com`
- Password: `password123`

### 3. Test Chat
1. Go to "Chat" page
2. Select a model
3. Send a message
4. Verify response from Groq API

### 4. Test RAG
1. Go to "RAG" page
2. Try querying (upload feature is mock for now)
3. Verify response

### 5. Check Dashboard
- View metrics
- Check token usage
- Verify charts display correctly

---

## 🐛 Troubleshooting

### Issue 1: "Cannot connect to backend"

**Solution:**
- Check backend service is running on Render
- Verify `API_URL` in frontend environment variables
- Check backend logs in Render dashboard

### Issue 2: "401 Unauthorized"

**Solution:**
- Check `SECRET_KEY` is set in backend
- Try logging out and logging in again
- Check JWT token expiration setting

### Issue 3: "Groq API Error"

**Solution:**
- Verify `GROQ_API_KEY` is correctly set
- Check API key is valid at https://console.groq.com
- Check Groq API rate limits

### Issue 4: "Service Unavailable"

**Solution:**
- Wait 1 minute (Render free tier may sleep after 15 min inactivity)
- Refresh the page
- Check Render service status

### Issue 5: Slow First Load

**Reason**: Render free tier sleeps after 15 minutes of inactivity

**Solution**: 
- First request may take 30-60 seconds
- Consider upgrading to paid plan for always-on service

---

## 📊 Render Free Tier Limits

- ✅ **Free forever**
- ✅ **750 hours/month** (enough for testing)
- ⚠️ **Services sleep after 15 min inactivity**
- ⚠️ **First request after sleep takes ~30-60 seconds**
- ✅ **Automatic HTTPS**
- ✅ **Automatic deployments from GitHub**

---

## 🔄 Update Deployment

### Push Updates to GitHub

```bash
cd c:\Users\hasin\OneDrive\Documents\llmops

# Make changes to your code

# Add and commit
git add llmops-platform/
git commit -m "Update deployment configuration"

# Push to GitHub
git push origin main
```

### Render Auto-Deploys

- Render automatically detects GitHub pushes
- Services rebuild and redeploy automatically
- Check deployment status in Render dashboard

---

## 🎯 Production Checklist

Before going to production:

- [ ] Change `SECRET_KEY` to strong random value
- [ ] Set up MongoDB for persistent storage
- [ ] Configure proper CORS settings
- [ ] Add rate limiting
- [ ] Set up monitoring and alerts
- [ ] Configure custom domain (optional)
- [ ] Enable HTTPS (automatic on Render)
- [ ] Set up backup strategy
- [ ] Document API endpoints
- [ ] Add logging and error tracking

---

## 💰 Cost Optimization

### Free Tier (Good for Testing)
- Backend + Frontend: **$0/month**
- Limited to 750 hours combined
- Services sleep after 15 min inactivity

### Starter Plan ($7/month each service)
- Always-on services
- No sleep time
- Faster response times
- Total: **$14/month** for both services

### Pro Plan ($25/month each service)
- More resources
- Better performance
- Priority support
- Total: **$50/month** for both services

---

## 📝 Useful Commands

### View Logs
```bash
# On Render dashboard
1. Go to service
2. Click "Logs" tab
3. View real-time logs
```

### Restart Service
```bash
# On Render dashboard
1. Go to service
2. Click "Manual Deploy" → "Clear build cache & deploy"
```

### Check Health
```bash
# Backend health check
curl https://llmops-backend.onrender.com/health

# Expected response:
# {"status": "healthy", "timestamp": "2026-06-07T..."}
```

---

## 🌐 Custom Domain (Optional)

### Add Custom Domain to Frontend

1. In Render dashboard → Frontend service
2. Click "Settings" → "Custom Domains"
3. Add your domain (e.g., `app.yourdomain.com`)
4. Update DNS records as instructed
5. Render provides automatic HTTPS

---

## 📧 Support & Resources

- **Render Documentation**: https://render.com/docs
- **Streamlit Documentation**: https://docs.streamlit.io
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **Groq API Documentation**: https://console.groq.com/docs

---

## 🎉 Success!

Your LLMOps Platform is now deployed and accessible worldwide! 🚀

**Frontend URL**: https://llmops-frontend.onrender.com
**Backend API**: https://llmops-backend.onrender.com
**API Docs**: https://llmops-backend.onrender.com/docs

---

## 🔐 Security Notes

1. **Never commit secrets** to Git
2. Use environment variables for all sensitive data
3. Rotate API keys regularly
4. Monitor usage and costs
5. Set up rate limiting for production
6. Use strong passwords
7. Enable 2FA on Render account

---

## 📈 Next Steps

1. ✅ Deploy to Render
2. ✅ Test all features
3. 🔄 Set up MongoDB for persistence
4. 🔄 Add file upload functionality
5. 🔄 Implement real RAG with ChromaDB
6. 🔄 Add user authentication enhancements
7. 🔄 Set up monitoring and alerts
8. 🔄 Configure custom domain
9. 🔄 Optimize performance
10. 🔄 Add more features!

---

**Happy Deploying! 🎊**
