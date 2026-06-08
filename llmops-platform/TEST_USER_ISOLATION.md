# 🧪 Test Plan: RAG User Isolation

## ✅ Fix Applied: RAG Metrics Now User-Specific

Previously, all users shared the same RAG metrics (localStorage). Now each user has their own isolated metrics stored on the backend.

---

## 🎯 Test Scenarios

### Test 1: New Account Shows Zero Metrics ✨

**Goal**: Verify new accounts start with clean slate (no old user's data)

**Steps**:
1. Open browser: http://localhost:3000
2. Click "Register" or go to http://localhost:3000/register
3. Create new account:
   - Email: `newuser@example.com`
   - Username: `newuser`
   - Password: `password123`
4. Click "Register"
5. Navigate to "Dashboard"

**Expected Result**:
```
RAG & Document Analytics Section:
├── Documents: 0 ✅
├── AI Queries: 0 ✅
└── Avg Latency: 0ms ✅

Chatbot vs RAG Usage:
├── Chatbot Requests: 0
└── RAG Queries: 0 ✅
```

**❌ FAIL If**: Shows numbers from previous user (e.g., 9 queries)
**✅ PASS If**: All metrics are 0 for new account

---

### Test 2: Upload Increments Only Current User's Count

**Goal**: Verify uploads are tracked per-user

**Steps**:
1. Stay logged in as `newuser@example.com`
2. Go to "Document RAG" page (http://localhost:3000/upload)
3. Upload a PDF file (any PDF)
4. Wait for success message
5. Go back to Dashboard

**Expected Result**:
```
RAG & Document Analytics:
├── Documents: 1 ✅ (incremented!)
├── AI Queries: 0 ✅ (unchanged)
└── Avg Latency: 0ms ✅
```

**❌ FAIL If**: Number doesn't change or changes incorrectly
**✅ PASS If**: Documents count = 1

---

### Test 3: Query Increments Only Current User's Count

**Goal**: Verify queries are tracked per-user

**Steps**:
1. Stay on Upload page
2. Type query: "What is machine learning?"
3. Select any model from dropdown
4. Click "Query with AI"
5. Wait for response
6. Go back to Dashboard

**Expected Result**:
```
RAG & Document Analytics:
├── Documents: 1 ✅
├── AI Queries: 1 ✅ (incremented!)
└── Avg Latency: ~50-200ms ✅ (shows query time)
```

**❌ FAIL If**: Query count doesn't increment
**✅ PASS If**: AI Queries = 1, Avg Latency shows time

---

### Test 4: User Switching Maintains Isolation

**Goal**: Verify different users see different metrics

**Part A - User A Activity**:
1. Logout (click "Logout" button)
2. Login as original user:
   - Email: `test@example.com`
   - Password: `password123`
3. Go to Dashboard
4. Note the metrics (probably has some activity already)
5. Go to Upload page
6. Perform 2 queries (any questions)
7. Note new query count

**Part B - Switch to User B**:
8. Logout
9. Login as `newuser@example.com` / `password123`
10. Go to Dashboard
11. Check RAG metrics

**Expected Result**:
```
User A (test@example.com):
├── Documents: X (whatever they had)
├── AI Queries: Y + 2 (old count + 2 new queries)
└── Avg Latency: Z ms

User B (newuser@example.com):
├── Documents: 1 ✅ (from Test 2)
├── AI Queries: 1 ✅ (from Test 3)
└── Avg Latency: ~100ms ✅ (from Test 3)
```

**❌ FAIL If**: User B shows User A's metrics
**✅ PASS If**: Each user sees only their own data

---

### Test 5: Multiple Sessions (Same User)

**Goal**: Verify user sees same data across browser tabs

**Steps**:
1. Login as `newuser@example.com` in Tab 1
2. Open new tab (Tab 2)
3. Go to http://localhost:3000 in Tab 2
4. Should auto-login or login with same account
5. Check Dashboard in both tabs

**Expected Result**:
Both tabs show **same metrics** for newuser:
- Documents: 1
- AI Queries: 1
- Latency: ~100ms

**❌ FAIL If**: Tabs show different numbers
**✅ PASS If**: Both tabs show identical metrics

---

### Test 6: Metrics Persist After Page Refresh

**Goal**: Verify metrics are stored on backend (not just in memory)

**Steps**:
1. Login as `newuser@example.com`
2. Note the Dashboard metrics
3. Refresh page (F5 or Ctrl+R)
4. Check metrics again

**Expected Result**:
Metrics remain the same after refresh:
- Documents: 1
- AI Queries: 1
- Latency: ~100ms

**❌ FAIL If**: Metrics reset to 0
**✅ PASS If**: Metrics unchanged after refresh

---

### Test 7: Backend API Verification

**Goal**: Verify backend returns correct user-specific data

**Steps**:
1. Login as `test@example.com`
2. Open browser DevTools (F12)
3. Go to Network tab
4. Navigate to Dashboard
5. Find request to `/metrics/rag`
6. Check response

**Expected Response**:
```json
{
  "total_uploads": X,
  "total_queries": Y,
  "avg_query_latency": Z.ZZ
}
```

**Then**:
7. Logout
8. Login as `newuser@example.com`
9. Go to Dashboard
10. Check `/metrics/rag` response again

**Expected Response**:
```json
{
  "total_uploads": 1,
  "total_queries": 1,
  "avg_query_latency": ~100
}
```

**❌ FAIL If**: Both users see same numbers
**✅ PASS If**: Each user gets different response

---

## 🎨 Visual Verification

### Before Fix (localStorage):
```
┌─────────────────────────────────────┐
│ User: test@example.com             │
│ RAG Queries: 9                      │ ← Old data
└─────────────────────────────────────┘
           ↓ Logout
           ↓ Login as newuser@example.com
┌─────────────────────────────────────┐
│ User: newuser@example.com          │
│ RAG Queries: 9                      │ ← WRONG! Shows old user's data
└─────────────────────────────────────┘
```

### After Fix (Backend API):
```
┌─────────────────────────────────────┐
│ User: test@example.com             │
│ RAG Queries: 9                      │ ← User A's data
└─────────────────────────────────────┘
           ↓ Logout
           ↓ Login as newuser@example.com
┌─────────────────────────────────────┐
│ User: newuser@example.com          │
│ RAG Queries: 0                      │ ← CORRECT! Fresh start
└─────────────────────────────────────┘
```

---

## 📊 Quick Test Summary

| Test # | Scenario | Pass Criteria |
|--------|----------|---------------|
| 1 | New account | Shows 0 uploads, 0 queries |
| 2 | Upload document | Count increments for that user only |
| 3 | Perform query | Query count increments correctly |
| 4 | Switch users | Each user sees only their data |
| 5 | Multiple tabs | Same user sees same data |
| 6 | Page refresh | Metrics persist (not lost) |
| 7 | API response | Backend returns user-specific data |

---

## 🚨 Common Issues to Check

### Issue 1: Metrics Still Showing Old Data
**Cause**: Frontend might be caching
**Fix**: Hard refresh (Ctrl+Shift+R) or clear browser cache

### Issue 2: Metrics Not Updating
**Cause**: Backend might not be restarted
**Fix**: Check backend terminal, restart if needed

### Issue 3: API 401 Unauthorized
**Cause**: Token expired or not logged in
**Fix**: Logout and login again

### Issue 4: Metrics Reset to Zero Unexpectedly
**Cause**: Backend restarted (in-memory storage cleared)
**Fix**: Normal behavior for current setup, will be fixed with MongoDB persistence

---

## 🔍 Debugging Tools

### Check Backend Logs:
```bash
# Backend terminal should show:
INFO: 127.0.0.1:XXXXX - "GET /metrics/rag HTTP/1.1" 200 OK
```

### Check Browser Console:
```javascript
// Open DevTools Console (F12)
// Should NOT see localStorage usage like:
localStorage.getItem('rag_metrics')  // ❌ OLD WAY

// Should see API calls:
GET /metrics/rag  // ✅ NEW WAY
```

### Check Network Tab:
1. Open DevTools (F12)
2. Go to Network tab
3. Filter: `rag`
4. Should see: `GET /metrics/rag` with 200 status

---

## ✅ Final Verification Checklist

Before marking as complete, verify:

- [ ] New accounts start with 0 metrics
- [ ] Upload increments document count
- [ ] Query increments query count and updates latency
- [ ] Different users see different metrics
- [ ] Same user sees same metrics across tabs
- [ ] Metrics persist after page refresh
- [ ] Backend API returns user-specific data
- [ ] No localStorage usage for RAG metrics
- [ ] No console errors in browser

---

## 🎉 Success Criteria

**Fix is successful when**:
1. ✅ New user account shows zero RAG metrics
2. ✅ Old user account shows their historical data
3. ✅ Switching users shows correct isolated data
4. ✅ No sharing of data between users
5. ✅ All tests pass

---

## 📞 Need Help?

**If tests fail**:
1. Check both servers are running (backend port 8000, frontend port 3000)
2. Clear browser cache and hard refresh
3. Check browser console for errors
4. Check backend terminal for error messages
5. Review `RAG_USER_ISOLATION_FIX.md` for implementation details

**Servers**:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

**Test Accounts**:
- Existing: test@example.com / password123
- New: Create any email / password123

---

**Ready to test!** Start with Test 1 and work through each scenario. 🚀
