# 🔐 How to Login - Step by Step Guide

## ✅ Backend is Running with Static Password

The backend is now using a **static password hash** that won't change on restart.

---

## 🎯 Login Steps

### Step 1: Clear Browser Data (IMPORTANT!)
The old authentication tokens in your browser are invalid. You must clear them:

**Option A - Clear Site Data (Recommended)**:
1. Open http://localhost:3000
2. Press `F12` to open DevTools
3. Go to "Application" tab (Chrome/Edge) or "Storage" tab (Firefox)
4. Click "Clear site data" or "Clear storage"
5. Refresh the page (`F5`)

**Option B - Clear Browser Cache**:
1. Press `Ctrl + Shift + Delete`
2. Select "Cookies and other site data"
3. Select "Cached images and files"
4. Click "Clear data"

**Option C - Use Incognito/Private Mode**:
1. Press `Ctrl + Shift + N` (Chrome/Edge) or `Ctrl + Shift + P` (Firefox)
2. Go to http://localhost:3000

---

### Step 2: Login

**URL**: http://localhost:3000

**Credentials**:
```
Email:    test@example.com
Password: password123
```

**Click "Sign in"**

---

### Step 3: If Login Still Fails

### Try Creating a New Account:

1. Go to: http://localhost:3000/register
2. Fill in:
   - Email: your.email@example.com
   - Username: yourusername
   - Password: yourpassword
3. Click "Create account"
4. Login with your new credentials

---

## 🔍 Troubleshooting

### Issue 1: "Incorrect email or password"

**Solutions**:
1. **Clear browser cache** (most common fix)
2. **Use incognito mode**
3. **Create new account** at /register
4. Check backend is running on port 8000

### Issue 2: Cannot reach server

**Check Backend Status**:
```bash
# Open: http://localhost:8000/health
# Should show: {"status":"healthy"...}
```

If not responding:
```bash
cd backend
venv\Scripts\python.exe app/main_simple.py
```

### Issue 3: Frontend not loading

**Check Frontend Status**:
```bash
# Frontend should be on: http://localhost:3000
```

If not responding:
```bash
cd frontend
npm run dev
```

---

## 💡 Why This Happens

### The Problem:
- Backend stores users in **memory** (RAM)
- When backend restarts, it creates fresh password hashes
- Old JWT tokens in browser become invalid
- Login fails with "incorrect password"

### The Solution:
- Now using **static password hash**
- Hash doesn't change on restart
- But you still need to **clear old tokens** from browser

---

## ✅ Verification Steps

### Test if Backend is Working:

**1. Check Health**:
```
Open: http://localhost:8000/health
Should see: {"status":"healthy",...}
```

**2. Check API Docs**:
```
Open: http://localhost:8000/docs
Should see Swagger UI
```

**3. Try Login API Directly**:
Open http://localhost:8000/docs
- Find "POST /auth/login"
- Click "Try it out"
- Enter:
  ```json
  {
    "email": "test@example.com",
    "password": "password123"
  }
  ```
- Click "Execute"
- Should get 200 response with token

---

## 🎯 Recommended Solution: Use Incognito Mode

The **easiest** way to test login:

1. Open Incognito/Private window
   - Chrome/Edge: `Ctrl + Shift + N`
   - Firefox: `Ctrl + Shift + P`

2. Go to http://localhost:3000

3. Login with:
   - Email: test@example.com
   - Password: password123

4. Should work immediately! ✅

---

## 🗄️ Long-Term Fix: Use MongoDB

To avoid these issues completely:

### Why MongoDB?
- ✅ Data persists across restarts
- ✅ No password hash regeneration
- ✅ No token invalidation
- ✅ Production-ready

### How to Switch:

**Current**: Using `main_simple.py` (in-memory)
**Better**: Use `main_mongo.py` (persistent)

**Steps**:
1. Ensure MongoDB is running
2. Stop current backend
3. Start MongoDB backend:
   ```bash
   cd backend
   $env:PYTHONPATH='C:\Users\hasin\OneDrive\Documents\llmops\llmops-platform\backend'
   venv\Scripts\python.exe -m app.main_mongo
   ```

---

## 📋 Quick Reference

### Default Credentials:
- **Email**: test@example.com
- **Password**: password123

### URLs:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Register**: http://localhost:3000/register

### Clear Cache:
- **Chrome/Edge**: Ctrl + Shift + Delete
- **Firefox**: Ctrl + Shift + Delete
- **Incognito**: Ctrl + Shift + N

---

## ✅ Current Status

### Backend:
- ✅ Running on port 8000
- ✅ Using static password hash
- ✅ Default user available
- ✅ Password: password123

### What You Need to Do:
1. ✅ **Clear browser cache** or use incognito
2. ✅ Go to http://localhost:3000
3. ✅ Login with test@example.com / password123

---

## 🎉 Summary

**The Fix**: Static password hash implemented ✅
**Your Action**: Clear browser cache to remove old tokens
**Result**: Login should work!

### Try Now:
1. Open **Incognito window** (`Ctrl + Shift + N`)
2. Go to http://localhost:3000
3. Login: test@example.com / password123
4. Should work! 🚀

---

**If still having issues after clearing cache, create a new account at http://localhost:3000/register**
