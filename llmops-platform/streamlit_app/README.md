# Streamlit Frontend for LLMOps Platform

Modern, interactive frontend built with Streamlit for the LLMOps Monitoring Platform.

## Features

- 🔐 **Authentication** - Login and registration
- 💬 **Chat Interface** - Interact with multiple AI models
- 📄 **RAG System** - Upload and query documents
- 📊 **Analytics Dashboard** - Real-time metrics and charts
- 🎨 **Modern UI** - Clean, responsive design
- 📈 **Visualizations** - Interactive charts with Plotly

## Quick Start

### Local Development

1. **Install Dependencies**
```bash
cd streamlit_app
pip install -r requirements.txt
```

2. **Configure API URL**
Edit `.streamlit/secrets.toml`:
```toml
API_URL = "http://localhost:8000"
```

3. **Start the App**
```bash
streamlit run app.py
```

Or use the batch file:
```bash
start_local.bat
```

4. **Access the App**
Open browser: http://localhost:8501

### Default Login
- Email: `test@example.com`
- Password: `password123`

## Project Structure

```
streamlit_app/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   ├── config.toml       # Streamlit configuration
│   └── secrets.toml      # API URL and secrets
├── render.yaml           # Render deployment config
├── start_local.bat       # Windows start script
└── README.md            # This file
```

## Pages

### 1. Dashboard 📊
- Summary metrics (requests, tokens, latency, cost)
- Usage trends over time
- Model performance comparison
- Evaluation metrics

### 2. Chat 💬
- Select from multiple AI models
- Real-time responses
- Token and latency tracking
- Chat history
- Model information display

### 3. RAG 📄
- Upload PDF documents
- Query documents with AI
- Model selection for queries
- Source attribution
- Retrieval metrics

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_URL` | Backend API endpoint | `http://localhost:8000` |

## Deployment

### Deploy to Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Configure:
   - Root Directory: `llmops-platform/streamlit_app`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
4. Add environment variable: `API_URL=https://your-backend.onrender.com`
5. Deploy!

See [STREAMLIT_RENDER_DEPLOYMENT.md](../STREAMLIT_RENDER_DEPLOYMENT.md) for detailed instructions.

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Deploy from GitHub repository
4. Select `streamlit_app/app.py` as the main file
5. Add secrets in Streamlit Cloud dashboard:
   ```toml
   API_URL = "https://your-backend.onrender.com"
   ```
6. Deploy!

## Dependencies

- `streamlit==1.31.1` - Web framework
- `requests==2.31.0` - HTTP library
- `plotly==5.18.0` - Interactive charts
- `python-dotenv==1.0.0` - Environment variables

## Features in Detail

### Authentication
- JWT token-based authentication
- Secure password handling
- Session management
- Auto-logout on token expiration

### Chat Interface
- Multiple model support (Llama 3.3 70B, Llama 3.1 8B, Llama 4 Scout)
- Real-time streaming responses
- Token usage tracking
- Latency monitoring
- Chat history with metadata
- Clear chat functionality

### RAG System
- PDF upload (mock for demo)
- Document querying with AI
- Configurable retrieval parameters
- Source attribution
- Model selection for queries
- Query history

### Dashboard
- Real-time metrics
- Interactive charts
- Usage trends
- Model performance comparison
- Cost tracking
- Evaluation metrics (faithfulness, relevance, etc.)

## Customization

### Theme
Edit `.streamlit/config.toml` to customize colors:

```toml
[theme]
primaryColor = "#1f77b4"  # Blue
backgroundColor = "#FFFFFF"  # White
secondaryBackgroundColor = "#f0f2f6"  # Light gray
textColor = "#262730"  # Dark gray
font = "sans serif"
```

### API Endpoint
Change `API_URL` in `.streamlit/secrets.toml` or set as environment variable.

## Troubleshooting

### "Cannot connect to backend"
- Check backend is running
- Verify `API_URL` is correct
- Check CORS settings on backend

### "401 Unauthorized"
- Check backend JWT secret key
- Try logging out and in again
- Clear browser cache

### Slow Performance
- Check backend response times
- Verify API key is configured
- Check network connection

## Development

### Add New Page
1. Create new function in `app.py`:
```python
def new_page():
    st.title("New Page")
    # Your content here
```

2. Add navigation button in sidebar:
```python
if st.button("🆕 New Page"):
    st.session_state.page = 'new_page'
    st.rerun()
```

3. Add page routing in main():
```python
elif st.session_state.page == 'new_page':
    new_page()
```

### Add New API Endpoint
Use the `api_request` helper function:
```python
response = api_request("/your/endpoint", method="POST", data={...})
if response:
    # Handle response
    st.success("Success!")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

MIT License - see [LICENSE](../LICENSE) file

## Support

For issues and questions:
- Check [STREAMLIT_RENDER_DEPLOYMENT.md](../STREAMLIT_RENDER_DEPLOYMENT.md)
- Review [QUICKSTART.md](../QUICKSTART.md)
- Create an issue on GitHub

---

**Built with ❤️ using Streamlit**
