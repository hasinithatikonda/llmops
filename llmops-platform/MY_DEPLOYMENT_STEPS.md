# 🚀 YOUR DEPLOYMENT CHECKLIST

Follow these steps to deploy your LLMOps Platform to Render.

---

## ✅ PREPARATION (You have everything ready!)

- [x] GitHub Repository: https://github.com/hasinithatikonda/llmops.git
- [x] Groq API Key: `[Get from your backend/.env file]`
- [x] Application tested locally and working perfectly
- [ ] Render account (create in Step 1)

---

## STEP 1: CREATE RENDER ACCOUNT (2 minutes)

1. Go to: https://render.com/signup
2. Click **"Sign up with GitHub"** (easiest option)
3. Authorize Render to access your repositories
4. ✅ You're in! Now you'll see the Render Dashboard

---

## STEP 2: DEPLOY BACKEND (4 minutes)

### 2.1 Create Web Service

1. In Render Dashboard, click the **blue "New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Build and deploy from a Git repository"** → Click **"Next"**

### 2.2 Connect Repository

1. Find and click: **"hasinithatikonda/llmops"**
   - If you don't see it, click "Configure account" to grant access
2. Click **"Connect"**

### 2.3 Configure Backend

Fill in the form with these **EXACT** values:

| Field | Value |
|-------|-------|
| **Name** | `llmops-backend` |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Root Directory** | `llmops-platform/backend` |
| **Runtime** | `Python 3` (auto-detected) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main_simple:app --host 0.0.0.0 --port $PORT` |

### 2.4 Add Environment Variables

Scroll down and click **"Advanced"** button

Click **"Add Environment Variable"** and add these **5 variables**:

**Variable 1:**
```
Key: SECRET_KEY
Value: dev-secret-key-change-in-production-use-random-string
```

**Variable 2:**
```
Key: ALGORITHM
Value: HS256
```

**Variable 3:**
```
Key: ACCESS_TOKEN_EXPIRE_MINUTES
Value: 30
```

**Variable 4:**
```
Key: GROQ_API_KEY
Value: [PASTE YOUR GROQ API KEY FROM backend/.env FILE]
```

**Variable 5:**
```
Key: FRONTEND_URL
Value: https://llmops-frontend.onrender.com
```
(We'll update this after deploying frontend)

### 2.5 Select Plan

- Scroll down to **"Instance Type"**
- Select **"Free"** (already selected by default)

### 2.6 Deploy!

1. Click the big **"Create Web Service"** button at the bottom
2. You'll see the deployment logs scrolling
3. Wait 3-5 minutes for deployment to complete
4. Look for **"Your service is live 🎉"** message

### 2.7 Copy Your Backend URL

At the top of the page, you'll see your URL like:
```
https://llmops-backend-XXXX.onrender.com
```

**COPY THIS URL** - You'll need it for the frontend!

Write it here: _______________________________________________

---

## STEP 3: DEPLOY FRONTEND (4 minutes)

### 3.1 Create Another Web Service

1. Click **"New +"** button again (top right)
2. Select **"Web Service"**
3. Click **"Build and deploy from a Git repository"** → **"Next"**

### 3.2 Connect Same Repository

1. Click: **"hasinithatikonda/llmops"** (same repo)
2. Click **"Connect"**

### 3.3 Configure Frontend

Fill in with these **EXACT** values:

| Field | Value |
|-------|-------|
| **Name** | `llmops-frontend` |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Root Directory** | `llmops-platform/streamlit_app` |
| **Runtime** | `Python 3` (auto-detected) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0` |

### 3.4 Add Environment Variable

Click **"Advanced"** button

Click **"Add Environment Variable"**:

**Variable 1:**
```
Key: API_URL
Value: [PASTE YOUR BACKEND URL FROM STEP 2.7 HERE]
```

Example: `https://llmops-backend-abc123.onrender.com`

### 3.5 Select Plan

- Select **"Free"** instance type

### 3.6 Deploy!

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Look for **"Your service is live 🎉"**

### 3.7 Copy Your Frontend URL

At the top, you'll see:
```
https://llmops-frontend-XXXX.onrender.com
```

**COPY THIS URL** - This is your app!

Write it here: _______________________________________________

---

## STEP 4: UPDATE BACKEND FRONTEND_URL (1 minute)

Now we need to tell the backend about the real frontend URL:

1. Go back to your **backend service** (click "Dashboard" then "llmops-backend")
2. Click **"Environment"** in the left sidebar
3. Find the `FRONTEND_URL` variable
4. Click **"Edit"** (pencil icon)
5. Change the value to your **actual frontend URL from Step 3.7**
   - Example: `https://llmops-frontend-abc123.onrender.com`
6. Click **"Save Changes"**
7. Service will automatically redeploy (wait 1-2 minutes)

---

## STEP 5: TEST YOUR DEPLOYMENT! 🎉

### 5.1 Open Your App

1. Go to your frontend URL from Step 3.7
2. Wait 30-60 seconds if it's the first time (free tier waking up)
3. You should see the LLMOps Platform login page!

### 5.2 Login

```
Email: test@example.com
Password: password123
```

### 5.3 Test Features

✅ Dashboard - Check metrics and charts
✅ Chat - Try sending a message (select a model first)
✅ RAG - Try the query feature

---

## 🎊 SUCCESS! YOU'RE DEPLOYED!

Your live URLs:

**Frontend (Your App):**
- URL: https://llmops-frontend-XXXX.onrender.com
- Login: test@example.com / password123

**Backend (API):**
- URL: https://llmops-backend-XXXX.onrender.com
- API Docs: https://llmops-backend-XXXX.onrender.com/docs

**Features:**
✅ Public access from anywhere
✅ HTTPS encryption
✅ Auto-deploy from GitHub
✅ Free hosting

---

## 📱 SHARE YOUR APP

You can now share your frontend URL with anyone!

---

## ⚠️ IMPORTANT NOTES

### Free Tier Behavior
- Services **sleep after 15 minutes** of inactivity
- **First request** after sleep takes 30-60 seconds to wake up
- Perfect for testing and demos!

### Keep It Always On
To prevent sleeping, upgrade to **Starter plan** ($7/month per service = $14 total)
- Go to service → Settings → Instance Type → Select "Starter"

### Auto-Deploy
- Any push to `main` branch in GitHub automatically deploys
- Check deployment status in Render dashboard

---

## 🐛 TROUBLESHOOTING

### Problem: "Cannot connect to backend"
**Solution**: Wait 60 seconds - service is waking up from sleep

### Problem: "401 Unauthorized"
**Solution**: 
1. Check backend logs (Dashboard → llmops-backend → Logs)
2. Try logging out and back in
3. Try incognito/private browsing mode

### Problem: "Groq API Error"
**Solution**: 
1. Go to backend → Environment
2. Verify `GROQ_API_KEY` is correct
3. Check if key is still valid at https://console.groq.com/keys

### Problem: "Service failed to start"
**Solution**:
1. Click on the failed service
2. Click "Logs" tab
3. Read the error message
4. Common fixes:
   - Check Root Directory path is correct
   - Verify Start Command is correct
   - Check all environment variables are set

---

## 📊 MONITORING YOUR APP

### View Logs
1. Go to Dashboard
2. Click on service name
3. Click "Logs" tab
4. See real-time application logs

### Check Metrics
1. Go to service
2. Click "Metrics" tab
3. See CPU, memory, request count

### Redeploy
1. Go to service
2. Click "Manual Deploy" button
3. Select "Clear build cache & deploy"

---

## 🔄 UPDATING YOUR APP

To deploy changes:

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```
3. Render automatically detects and deploys!
4. Check deployment progress in Render dashboard

---

## 🎯 NEXT STEPS

Now that you're deployed:

1. ✅ Test all features thoroughly
2. ✅ Share URL with friends/team
3. ✅ Monitor usage in Render dashboard
4. 🔄 Consider upgrading to Starter plan if needed
5. 🔄 Add custom domain (optional)
6. 🔄 Set up MongoDB for data persistence
7. 🔄 Add more features!

---

## 💡 PRO TIPS

1. **Bookmark your URLs** - Save both frontend and backend URLs
2. **Check logs regularly** - Catch issues early
3. **Monitor usage** - Stay within free tier limits (750 hrs/month)
4. **Keep API key secret** - Never commit to Git
5. **Test before sharing** - Make sure everything works

---

## 📞 NEED HELP?

- **Render Documentation**: https://render.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **Check your logs** in Render dashboard
- **Review** STREAMLIT_RENDER_DEPLOYMENT.md for detailed troubleshooting

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] Created Render account
- [ ] Deployed backend service
- [ ] Copied backend URL
- [ ] Deployed frontend service
- [ ] Copied frontend URL
- [ ] Updated backend FRONTEND_URL
- [ ] Tested login
- [ ] Tested chat feature
- [ ] Tested dashboard
- [ ] Bookmarked URLs
- [ ] Shared with team (optional)

---

**You're all set! Happy deploying! 🚀**

If you encounter any issues, check the Troubleshooting section or review the logs in Render dashboard.
