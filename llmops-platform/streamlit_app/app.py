"""
Streamlit Frontend for LLMOps Monitoring Platform
"""
import streamlit as st
import requests
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Configuration
API_URL = st.secrets.get("API_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="LLMOps Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# API Helper Functions
def api_request(endpoint, method="GET", data=None, auth=True):
    """Make API request with authentication"""
    url = f"{API_URL}{endpoint}"
    headers = {}
    
    if auth and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 401:
            st.session_state.token = None
            st.session_state.user = None
            st.error("Session expired. Please login again.")
            return None
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def login(email, password):
    """Login user"""
    data = {"email": email, "password": password}
    result = api_request("/auth/login", method="POST", data=data, auth=False)
    
    if result:
        st.session_state.token = result['access_token']
        st.session_state.user = result['user']
        st.session_state.page = 'dashboard'
        st.success("Login successful!")
        st.rerun()

def register(email, username, password):
    """Register new user"""
    data = {"email": email, "username": username, "password": password}
    result = api_request("/auth/register", method="POST", data=data, auth=False)
    
    if result:
        st.session_state.token = result['access_token']
        st.session_state.user = result['user']
        st.session_state.page = 'dashboard'
        st.success("Registration successful!")
        st.rerun()

def logout():
    """Logout user"""
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.page = 'login'
    st.rerun()

# Pages

def login_page():
    """Login and registration page"""
    st.markdown('<div class="main-header">🤖 LLMOps Platform</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_btn"):
            if email and password:
                login(email, password)
            else:
                st.error("Please fill in all fields")
        
        st.info("💡 Default account: test@example.com / password123")
    
    with tab2:
        st.subheader("Create New Account")
        reg_email = st.text_input("Email", key="reg_email")
        reg_username = st.text_input("Username", key="reg_username")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        
        if st.button("Register", key="reg_btn"):
            if reg_email and reg_username and reg_password:
                register(reg_email, reg_username, reg_password)
            else:
                st.error("Please fill in all fields")

def dashboard_page():
    """Dashboard with metrics and analytics"""
    st.title("📊 Dashboard")
    
    # Get metrics
    summary = api_request("/metrics/summary")
    usage = api_request("/metrics/usage?days=7")
    models = api_request("/metrics/models")
    evaluation = api_request("/metrics/evaluation")
    rag_metrics = api_request("/metrics/rag")
    
    if not summary:
        st.error("Failed to load metrics")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Requests", summary['total_requests'])
    with col2:
        st.metric("Active Models", summary['active_models'])
    with col3:
        st.metric("Avg Latency", f"{summary['average_latency']:.0f}ms")
    with col4:
        st.metric("Total Tokens", f"{summary['total_tokens']:,}")
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("Total Cost", f"${summary['total_cost']:.4f}")
    with col6:
        st.metric("Error Rate", f"{summary['error_rate']:.1f}%")
    with col7:
        if rag_metrics:
            st.metric("RAG Uploads", rag_metrics['total_uploads'])
    with col8:
        if rag_metrics:
            st.metric("RAG Queries", rag_metrics['total_queries'])
    
    # Charts
    st.subheader("📈 Usage Trends")
    
    if usage:
        col1, col2 = st.columns(2)
        
        with col1:
            # Requests over time
            fig_requests = go.Figure()
            fig_requests.add_trace(go.Scatter(
                x=[u['date'] for u in usage],
                y=[u['requests'] for u in usage],
                mode='lines+markers',
                name='Requests',
                line=dict(color='#1f77b4', width=3)
            ))
            fig_requests.update_layout(
                title="Daily Requests",
                xaxis_title="Date",
                yaxis_title="Requests",
                height=300
            )
            st.plotly_chart(fig_requests, use_container_width=True)
        
        with col2:
            # Tokens over time
            fig_tokens = go.Figure()
            fig_tokens.add_trace(go.Scatter(
                x=[u['date'] for u in usage],
                y=[u['tokens'] for u in usage],
                mode='lines+markers',
                name='Tokens',
                line=dict(color='#ff7f0e', width=3)
            ))
            fig_tokens.update_layout(
                title="Daily Token Usage",
                xaxis_title="Date",
                yaxis_title="Tokens",
                height=300
            )
            st.plotly_chart(fig_tokens, use_container_width=True)
    
    # Model metrics
    st.subheader("🤖 Model Performance")
    
    if models:
        model_data = {
            'Model': [m['model'].split('/')[-1] for m in models],
            'Requests': [m['requests'] for m in models],
            'Tokens': [m['tokens'] for m in models],
            'Avg Latency (ms)': [m['avg_latency'] for m in models]
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Model requests pie chart
            fig_pie = go.Figure(data=[go.Pie(
                labels=model_data['Model'],
                values=model_data['Requests'],
                hole=.3
            )])
            fig_pie.update_layout(title="Requests by Model", height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Model latency bar chart
            fig_bar = go.Figure(data=[go.Bar(
                x=model_data['Model'],
                y=model_data['Avg Latency (ms)'],
                marker_color='lightblue'
            )])
            fig_bar.update_layout(title="Avg Latency by Model", height=300)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Evaluation metrics
    if evaluation and evaluation['avg_ragas_score'] > 0:
        st.subheader("🎯 Evaluation Metrics")
        
        eval_col1, eval_col2, eval_col3, eval_col4, eval_col5, eval_col6 = st.columns(6)
        
        with eval_col1:
            st.metric("Faithfulness", f"{evaluation['avg_faithfulness']:.2f}")
        with eval_col2:
            st.metric("Relevance", f"{evaluation['avg_relevance']:.2f}")
        with eval_col3:
            st.metric("Precision", f"{evaluation['avg_context_precision']:.2f}")
        with eval_col4:
            st.metric("Recall", f"{evaluation['avg_context_recall']:.2f}")
        with eval_col5:
            st.metric("Hallucination", f"{evaluation['avg_hallucination_risk']:.2f}")
        with eval_col6:
            st.metric("RAGAS Score", f"{evaluation['avg_ragas_score']:.2f}")

def chat_page():
    """Chat interface"""
    st.title("💬 Chat with AI")
    
    # Get available models
    models = api_request("/models")
    
    if models:
        model_options = {f"{m['name']} ({m['speed']})": m['id'] for m in models}
        selected_model_name = st.selectbox(
            "Select Model",
            options=list(model_options.keys()),
            help="Choose the AI model for your conversation"
        )
        selected_model = model_options[selected_model_name]
        
        # Show model info
        model_info = next((m for m in models if m['id'] == selected_model), None)
        if model_info:
            with st.expander("ℹ️ Model Information"):
                st.write(f"**Description:** {model_info['description']}")
                st.write(f"**Context Window:** {model_info['context_window']:,} tokens")
                st.write(f"**Max Output:** {model_info['max_tokens']:,} tokens")
                st.write(f"**Speed:** {model_info['speed']}")
    else:
        selected_model = "llama-3.3-70b-versatile"
    
    # Chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "metadata" in message:
                with st.expander("Details"):
                    st.caption(f"Model: {message['metadata']['model']}")
                    st.caption(f"Tokens: {message['metadata']['tokens']}")
                    st.caption(f"Latency: {message['metadata']['latency']}ms")
    
    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                data = {
                    "message": prompt,
                    "model": selected_model
                }
                response = api_request("/chat", method="POST", data=data)
                
                if response:
                    st.write(response['response'])
                    
                    # Add assistant message with metadata
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response['response'],
                        "metadata": {
                            "model": response['model'],
                            "tokens": response['tokens_used'],
                            "latency": response['latency_ms']
                        }
                    })
                    
                    with st.expander("Details"):
                        st.caption(f"Model: {response['model']}")
                        st.caption(f"Tokens: {response['tokens_used']}")
                        st.caption(f"Latency: {response['latency_ms']:.2f}ms")
                else:
                    st.error("Failed to get response")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

def rag_page():
    """RAG (Upload and Query) interface"""
    st.title("📄 RAG - Document Q&A")
    
    tab1, tab2 = st.tabs(["📤 Upload Documents", "❓ Query Documents"])
    
    with tab1:
        st.subheader("Upload PDF Documents")
        
        uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
        
        if uploaded_file:
            if st.button("Upload and Process"):
                with st.spinner("Processing document..."):
                    # Simulate upload
                    response = api_request("/upload/pdf", method="POST", data={})
                    
                    if response:
                        st.success(f"✅ {response['message']}")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Pages", response['pages'])
                        with col2:
                            st.metric("Chunks", response['chunks'])
                        with col3:
                            st.metric("Status", "Indexed")
    
    with tab2:
        st.subheader("Query Your Documents")
        
        # Get available models
        models = api_request("/models")
        
        if models:
            model_options = {f"{m['name']} ({m['speed']})": m['id'] for m in models}
            selected_model_name = st.selectbox(
                "Select Model for RAG",
                options=list(model_options.keys()),
                help="Choose the AI model for document queries",
                key="rag_model"
            )
            selected_model = model_options[selected_model_name]
        else:
            selected_model = "llama-3.3-70b-versatile"
        
        query = st.text_area("Enter your question about the documents", height=100)
        n_results = st.slider("Number of relevant chunks to retrieve", 1, 10, 3)
        
        if st.button("🔍 Search"):
            if query:
                with st.spinner("Searching documents..."):
                    response = api_request(
                        f"/upload/query?query={query}&n_results={n_results}&model={selected_model}",
                        method="POST"
                    )
                    
                    if response:
                        st.success("✅ Query completed!")
                        
                        # Display answer
                        st.markdown("### 📝 Answer")
                        st.info(response['response'])
                        
                        # Display sources
                        st.markdown("### 📚 Sources")
                        for i, source in enumerate(response['sources'], 1):
                            st.caption(f"{i}. {source}")
                        
                        # Display model used
                        st.caption(f"🤖 Model: {selected_model}")
            else:
                st.warning("Please enter a question")

# Sidebar
def sidebar():
    """Sidebar navigation"""
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/1f77b4/FFFFFF?text=LLMOps", use_container_width=True)
        
        if st.session_state.user:
            st.success(f"👤 {st.session_state.user['username']}")
            st.caption(f"📧 {st.session_state.user['email']}")
            
            st.divider()
            
            # Navigation
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
            
            if st.button("💬 Chat", use_container_width=True):
                st.session_state.page = 'chat'
                st.rerun()
            
            if st.button("📄 RAG", use_container_width=True):
                st.session_state.page = 'rag'
                st.rerun()
            
            st.divider()
            
            if st.button("🚪 Logout", use_container_width=True):
                logout()
        else:
            st.info("Please login to continue")
            st.caption("Default account:")
            st.code("test@example.com\npassword123")

# Main app
def main():
    """Main application"""
    sidebar()
    
    if not st.session_state.token:
        login_page()
    else:
        if st.session_state.page == 'dashboard':
            dashboard_page()
        elif st.session_state.page == 'chat':
            chat_page()
        elif st.session_state.page == 'rag':
            rag_page()
        else:
            dashboard_page()

if __name__ == "__main__":
    main()
