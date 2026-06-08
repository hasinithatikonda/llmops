# ⚡ Quick Deploy Guide - 5 Minutes

Get your LLMOps Platform deployed to Render in 5 minutes!

---

## Prerequisites ✅
- [x] GitHub repository: https://github.com/hasinithatikonda/llmops.git
- [ ] Render account: https://render.com (sign up - FREE)
- [ ] Groq API key: https://console.groq.com/keys (get one - FREE)

---

## Step 1: Deploy Backend (2 minutes) 🔧

1. Go to https://render.com → Click **"New+"** → **"Web Service"**
2. Connect GitHub: `hasinithatikonda/llmops`
3. Fill in:
   ```
   Name: llmops-backend
   Root Directory: llmops-platform/backend
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main_simple:app --host 0.0.0.0 --port $PORT
   ```
4. Add Environment Variables:
   ```
   SECRET_KEY = any-random-string-here-12345
   GROQ_API_KEY = gsk_your_key_here
   FRONTEND_URL = https://llmops-frontend.onrender.com
   ```
5. Click **"Create Web Service"**
6. **Copy your backend URL**: `https://llmops-backend.onrender.com`

---

## Step 2: Deploy Frontend (2 minutes) 🎨

1. Click **"New+"** → **"Web Service"** again
2. Same GitHub repo: `hasinithatikonda/llmops`
3. Fill in:
   ```
   Name: llmops-frontend
   Root Directory: llmops-platform/streamlit_app
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
4. Add Environment Variable:
   ```
   API_URL = https://llmops-backend.onrender.com
   ```
   (Use YOUR backend URL from Step 1!)
5. Click **"Create Web Service"**

---

## Step 3: Update Backend (30 seconds) 🔄

1. Go back to backend service
2. Environment → Update `FRONTEND_URL`:
   ```
   FRONTEND_URL = https://llmops-frontend.onrender.com
   ```
   (Use YOUR frontend URL from Step 2!)
3. Save → Service will auto-redeploy

---

## Step 4: Test (30 seconds) ✅

1. Open **your frontend URL**
2. Login with:
   ```
   Email: test@example.com
   Password: password123
   ```
3. Try chatting!
4. Check dashboard!

---

## 🎉 Done!

**Your URLs:**
- Frontend: `https://llmops-frontend.onrender.com`
- Backend: `https://llmops-backend.onrender.com`
- API Docs: `https://llmops-backend.onrender.com/docs`

---

## ⚠️ Important Notes

### Free Tier Behavior
- Services sleep after 15 min inactivity
- First request takes ~30-60 seconds
- Perfect for testing!

### To Keep Always-On
Upgrade to Starter plan: $7/month per service ($14 total)

---

## 🐛 Troubleshooting

### "Can't connect to backend"
Wait 1 minute - free tier may be waking up

### "401 Unauthorized"
Clear browser cache, try incognito mode

### "Groq API Error"
Check your API key in backend environment variables

---

## 📚 More Help

- Full Guide: `STREAMLIT_RENDER_DEPLOYMENT.md`
- Frontend Docs: `streamlit_app/README.md`
- Troubleshooting: See full deployment guide

---

**That's it! You're deployed! 🚀**
