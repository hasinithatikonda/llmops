# LLMOps Platform - Testing Guide

## ✅ Current Status

### Backend (Port 8000)
- **Status**: ✅ Running
- **API Docs**: http://localhost:8000/docs
- **Groq Integration**: ✅ Configured and working
- **Available Models**: 5 models configured with different capabilities

### Frontend (Port 3000)
- **Status**: ✅ Running
- **URL**: http://localhost:3000
- **Pages**: Login, Register, Dashboard, Chat, Upload

## 🧪 How to Test

### 1. Authentication
1. Go to http://localhost:3000/login
2. Use credentials:
   - **Email**: `test@example.com`
   - **Password**: `password123`
3. You should be redirected to the dashboard

### 2. Model Selection & Chat
1. Navigate to **Chat** page
2. You should see a model selector dropdown in the top-right with 5 models:
   - **Llama 3.3 70B** (8000 tokens, medium speed)
   - **Llama 3.1 70B** (8000 tokens, medium speed)
   - **Llama 3.1 8B Instant** (8000 tokens, very fast)
   - **Mixtral 8x7B** (4096 tokens, fast)
   - **Gemma 2 9B** (2048 tokens, fast)

3. **Test Token Limits**: 
   - Select different models and verify the "Max tokens" display updates
   - Each model shows its specific token limit below the selector

4. **Test Chat**:
   - Select "Llama 3.3 70B"
   - Ask: "Explain machine learning in 2 sentences"
   - Wait for response (should be fast, 1-3 seconds)
   - Check the response includes:
     - ✅ Actual AI-generated answer (not mock data)
     - ✅ Latency (ms)
     - ✅ Cost ($)
     - ✅ Tokens used
     - ✅ Model name badge

5. **Test Model Comparison**:
   - Ask the same question with different models:
     - "What is quantum computing?" → Llama 3.3 70B
     - "What is quantum computing?" → Llama 3.1 8B Instant
     - "What is quantum computing?" → Mixtral 8x7B
   - Compare:
     - Response quality
     - Response speed (latency)
     - Token usage
     - Cost differences

### 3. Dashboard Metrics
1. Go to **Dashboard** page
2. After chatting, you should see **user-specific** metrics:
   - **Total Requests**: Your chat count
   - **Total Tokens**: Sum of all your chats
   - **Total Cost**: Calculated from your usage
   - **Avg Latency**: Average response time

3. **Model Performance Chart**:
   - Should show bars for each model you've used
   - Compare requests and latency across models
   - Models you haven't used yet won't show data

4. **Usage Trends**:
   - Daily breakdown of your activity
   - Shows requests per day
   - Token usage per day

### 4. Upload & Query
1. Go to **Upload** page
2. Upload a PDF (mock processing)
3. Query the "document":
   - Try: "What is machine learning?"
   - Try: "Explain Python programming"
   - Try: "Tell me about APIs"
   - Should get relevant responses with source citations

## 🎯 What to Verify

### ✅ Real AI Responses
- [ ] Chat responses are **actually from Groq API** (not mock data)
- [ ] Different models give **different responses**
- [ ] Responses are **relevant** to the question asked
- [ ] Response quality varies by model capability

### ✅ Model Selection
- [ ] Model dropdown shows all 5 models
- [ ] Can switch between models
- [ ] Max tokens display **changes** when model changes
- [ ] Model name appears in message metadata

### ✅ Performance Tracking
- [ ] Each chat tracks tokens, latency, and cost
- [ ] Dashboard shows **your** activity (not generic data)
- [ ] Model performance chart updates after using models
- [ ] Metrics are accurate and persistent during session

### ✅ Model Comparison
- [ ] **Llama 3.3 70B**: Best quality, moderate speed
- [ ] **Llama 3.1 8B Instant**: Fastest, simpler responses
- [ ] **Mixtral 8x7B**: Good balance
- [ ] Latency differences visible in dashboard

## 🔍 Expected Results

### Model Characteristics

| Model | Max Tokens | Expected Speed | Best For |
|-------|-----------|---------------|----------|
| Llama 3.3 70B | 8000 | Medium (~1-2s) | Complex tasks, detailed explanations |
| Llama 3.1 70B | 8000 | Medium (~1-2s) | General purpose, balanced |
| Llama 3.1 8B Instant | 8000 | Very Fast (<1s) | Quick answers, simple queries |
| Mixtral 8x7B | 4096 | Fast (~1s) | Balanced performance |
| Gemma 2 9B | 2048 | Fast (~1s) | Efficient, shorter responses |

### Cost Tracking
- Groq API cost: ~$0.0000002 per token
- A 100-token response costs ~$0.00002
- Dashboard tracks cumulative cost per user

## 🐛 Known Issues

1. **bcrypt warning**: Harmless warning on backend startup (doesn't affect functionality)
2. **First request slower**: First API call to each model may be slower (cold start)
3. **Session-based tracking**: Metrics reset if backend restarts

## 🚀 Next Steps

If all tests pass, the system is ready for:
1. Production Groq API key (if needed)
2. Database persistence (currently in-memory)
3. Advanced model comparison features
4. Model performance benchmarking
5. A/B testing capabilities

## 📊 API Endpoints

- `GET /models` - List available models
- `POST /chat` - Send chat message (with model parameter)
- `GET /metrics/summary` - User metrics summary
- `GET /metrics/models` - Per-model performance metrics
- `GET /metrics/usage` - Daily usage breakdown
- `GET /metrics/evaluation` - Quality metrics (mock)

## 🎓 Tips for Testing

1. **Test systematically**: Use same question across models for comparison
2. **Check token limits**: Verify max_tokens changes per model
3. **Monitor latency**: Faster models should show lower latency
4. **Track costs**: Each request adds to total cost
5. **Dashboard updates**: Refresh to see latest metrics
