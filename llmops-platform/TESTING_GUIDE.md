# Testing Guide - RAG Model Selection Feature

## 🎯 Quick Start Testing

### Prerequisites
✅ Backend running on: http://localhost:8000
✅ Frontend running on: http://localhost:3000
✅ Logged in with credentials: test@example.com / password123

---

## 📝 Test Scenarios

### Test 1: Model Dropdown Display ✨
**Goal**: Verify model names display without token numbers

**Steps**:
1. Navigate to http://localhost:3000/upload
2. Look at the "Select AI Model" dropdown
3. Click to open the dropdown

**Expected Result**:
- ✅ Dropdown shows 3 models
- ✅ Names shown: 
  - "Llama 3.3 70B Versatile"
  - "Llama 3.1 8B Instant"  
  - "Llama 4 Scout 17B Instruct"
- ✅ NO token numbers like "- 6000 tokens max" (removed as requested)
- ✅ Below dropdown shows description and speed

**Screenshot Location**: Should look clean and professional

---

### Test 2: Model Selection and Query 🔍
**Goal**: Verify different models can be selected and used for queries

**Steps**:
1. Go to http://localhost:3000/upload
2. Upload a PDF (drag & drop or click to upload)
3. Wait for success message
4. Select "Llama 3.3 70B Versatile" from dropdown
5. Type question: "What is machine learning?"
6. Click "Query with AI"
7. Wait for response
8. Note the model badge in the response

**Expected Result**:
- ✅ Response appears with AI answer
- ✅ Model badge shows "LLAMA 3.3 70B"
- ✅ Latency displays (e.g., "1250ms")
- ✅ "RAG Query" badge appears
- ✅ Response quality is good

**Repeat with other models**:
- Test with "Llama 3.1 8B Instant" (should be faster, simpler responses)
- Test with "Llama 4 Scout 17B" (balanced performance)

---

### Test 3: Model Performance Comparison ⚡
**Goal**: Compare response times and quality across models

**Test Data**:
```
Query: "What is machine learning?"
```

**Steps**:
1. Select "Llama 3.1 8B Instant"
2. Submit query, note latency
3. Select "Llama 3.3 70B Versatile"  
4. Submit same query, note latency
5. Select "Llama 4 Scout 17B"
6. Submit same query, note latency

**Expected Results**:
- ✅ 8B model: Fastest response (200-500ms typically)
- ✅ Scout 17B: Medium response time (400-800ms)
- ✅ 70B model: Slower but more detailed (800-1500ms)
- ✅ Each shows correct model badge
- ✅ All responses are relevant

---

### Test 4: Dashboard Analytics Update 📊
**Goal**: Verify RAG queries are tracked in analytics

**Steps**:
1. Note current RAG query count on dashboard
2. Go to /upload page
3. Perform 3 queries with different models
4. Return to http://localhost:3000/dashboard
5. Scroll to "RAG & Document Analytics" section

**Expected Result**:
- ✅ "AI Queries" count increased by 3
- ✅ "Documents" count shows uploads
- ✅ "Avg Latency" updated with new queries
- ✅ Charts show data if enough queries performed
- ✅ No errors in display

---

### Test 5: Response Badge Accuracy 🏷️
**Goal**: Ensure response shows correct model used

**Steps**:
1. Select "Llama 3.1 8B Instant"
2. Submit query
3. Check response badge

**Expected Result**:
- ✅ Badge shows: "LLAMA 3.1 8B" or similar
- ✅ NOT showing: "LLAMA 3.3" (different model)
- ✅ Badge color matches theme
- ✅ Badge is readable and clear

---

### Test 6: Model Info Display 📋
**Goal**: Verify model descriptions and speed indicators

**Steps**:
1. Go to /upload page
2. Select each model one by one
3. Read the text below the dropdown

**Expected for Each Model**:

**Llama 3.3 70B**:
- Description: "Most capable model, best for complex tasks and reasoning"
- Speed: "medium speed"

**Llama 3.1 8B**:
- Description: "Ultra-fast responses, great for simple queries and high-throughput"  
- Speed: "very fast speed"

**Llama 4 Scout 17B**:
- Description: "New Llama 4 model, optimized for instruction following"
- Speed: "fast speed"

---

### Test 7: Error Handling 🚨
**Goal**: Ensure errors are handled gracefully

**Scenarios to Test**:
1. **Empty query**: Try to submit without typing anything
   - ✅ Button should be disabled or show error
   
2. **Query before upload**: Query without uploading document
   - ✅ Should still work (mock responses)
   
3. **Network error**: Disconnect internet, try query
   - ✅ Should show error message

---

### Test 8: UI/UX Polish ✨
**Goal**: Verify visual design and user experience

**Checklist**:
- ✅ Dropdown has purple gradient styling
- ✅ Hover effects work smoothly
- ✅ Model selector is easy to click
- ✅ Text is readable (good contrast)
- ✅ Icons display correctly
- ✅ Responsive on mobile (test with DevTools)
- ✅ No layout shifts when selecting models
- ✅ Response area animates smoothly
- ✅ Performance badges look professional

---

## 🔧 Developer Testing

### Backend API Testing

**Test GET /models endpoint**:
```bash
curl http://localhost:8000/models
```

Expected: JSON array with 3 models, each with id, name, description, max_tokens, speed

**Test RAG Query with Model Parameter**:
```bash
curl -X POST "http://localhost:8000/upload/query?query=What%20is%20machine%20learning&model=llama-3.1-8b-instant&n_results=3" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Expected: JSON response with answer, sources, and query

---

### Browser Console Testing

**Check for errors**:
1. Open Chrome DevTools (F12)
2. Go to Console tab
3. Navigate through app
4. Perform queries

Expected:
- ✅ No red errors
- ✅ No warnings about missing dependencies
- ✅ API calls return 200 status codes

**Check Network requests**:
1. Open DevTools Network tab
2. Perform a query
3. Find POST request to `/upload/query`
4. Check request parameters

Expected:
- ✅ `query` parameter present
- ✅ `model` parameter present with selected model ID
- ✅ `n_results` parameter = 3
- ✅ Response status = 200

---

## 📱 Cross-Browser Testing

### Desktop Browsers:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Edge (latest)
- [ ] Safari (if on Mac)

### Mobile Testing:
- [ ] Chrome DevTools mobile simulation
- [ ] Actual mobile device (if available)
- [ ] Tablet view

**What to Check**:
- Dropdown works on mobile
- Text is readable without zooming
- Buttons are tap-friendly
- Layout doesn't break

---

## ✅ Acceptance Criteria

All features should meet these criteria:

### Functional:
- ✅ Model dropdown displays 3 models without token numbers
- ✅ Model selection persists during session
- ✅ Each model can process queries successfully
- ✅ Response shows correct model badge
- ✅ Latency metrics display accurately
- ✅ Dashboard tracks RAG queries
- ✅ No console errors or warnings

### Visual:
- ✅ Purple gradient theme consistent
- ✅ Text readable with good contrast
- ✅ Icons render correctly
- ✅ Animations smooth (no janking)
- ✅ Responsive on all screen sizes
- ✅ Professional appearance

### Performance:
- ✅ Page loads in < 2 seconds
- ✅ Model switching instant
- ✅ Query responses within reasonable time
- ✅ No memory leaks (test with multiple queries)
- ✅ Smooth scrolling and interactions

---

## 🐛 Known Issues to Watch For

### Potential Issues:
1. **Model not found**: If backend doesn't recognize model ID
   - Check: Model ID matches AVAILABLE_MODELS array
   
2. **Token limit exceeded**: If query too long for 8B model
   - Check: Backend uses correct max_tokens per model
   
3. **CORS errors**: If frontend can't reach backend
   - Check: Both servers running on correct ports
   
4. **Metrics not updating**: If localStorage quota exceeded
   - Check: Browser settings allow localStorage
   
5. **Badge showing wrong model**: If response doesn't match selection
   - Check: Backend returns model ID in response

---

## 📊 Test Results Template

```
TEST DATE: ___________
TESTER: ___________

| Test # | Test Name | Status | Notes |
|--------|-----------|--------|-------|
| 1 | Model Dropdown | ⬜ PASS / ⬜ FAIL | |
| 2 | Model Selection | ⬜ PASS / ⬜ FAIL | |
| 3 | Performance Compare | ⬜ PASS / ⬜ FAIL | |
| 4 | Dashboard Analytics | ⬜ PASS / ⬜ FAIL | |
| 5 | Response Badge | ⬜ PASS / ⬜ FAIL | |
| 6 | Model Info Display | ⬜ PASS / ⬜ FAIL | |
| 7 | Error Handling | ⬜ PASS / ⬜ FAIL | |
| 8 | UI/UX Polish | ⬜ PASS / ⬜ FAIL | |

Overall Status: ⬜ PASS / ⬜ FAIL
```

---

## 🚀 Next Steps After Testing

### If All Tests Pass:
1. ✅ Feature is ready for production
2. Document any edge cases discovered
3. Consider adding automated tests
4. Update user documentation
5. Deploy to staging environment

### If Tests Fail:
1. Document specific failures
2. Create bug tickets with details
3. Fix issues in order of severity
4. Re-test after fixes
5. Update this testing guide if needed

---

## 💡 Tips for Effective Testing

1. **Test in isolation**: Test one feature at a time
2. **Clear cache**: Between tests to avoid stale data
3. **Use incognito**: Fresh session for accurate results
4. **Take screenshots**: Document visual issues
5. **Note timestamps**: Record when issues occur
6. **Test edge cases**: Empty strings, special characters, long queries
7. **Performance testing**: Try 10+ queries in a row
8. **Mobile first**: Often reveals layout issues

---

## 📞 Support

If you encounter issues during testing:
1. Check browser console for errors
2. Check backend logs for API errors
3. Verify both servers are running
4. Clear browser cache and retry
5. Check environment variables in `.env`
6. Review `RAG_MODEL_SELECTION_SUMMARY.md` for implementation details

**Backend logs**: Check terminal running `python app/main_simple.py`
**Frontend logs**: Check terminal running `npm run dev`
**Browser logs**: Open DevTools Console (F12)

---

## ✅ Ready to Test!

Your application is running and ready for testing:
- 🌐 Frontend: http://localhost:3000
- 🔌 Backend: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

Start with Test 1 and work through each scenario systematically. Good luck! 🚀
