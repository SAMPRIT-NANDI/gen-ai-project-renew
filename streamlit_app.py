import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
from bs4 import BeautifulSoup
import os

# Configure page
st.set_page_config(
    page_title="AI Conversation Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Keep original beautiful theme
st.markdown("""
    <style>
    :root{
        --bg-1: #ffecd2;
        --bg-2: #fcb69f;
        --card: rgba(255,255,255,0.9);
        --muted: #5b5b6b;
        --accent-1: #00b4d8;
        --accent-2: #ff6b6b;
        --accent-3: #ffd166;
    }
    *{box-sizing: border-box;font-family: 'Inter', system-ui, sans-serif;}
    body {background: linear-gradient(135deg, var(--bg-1) 0%, var(--bg-2) 100%);}
    .stApp > div:first-child {padding: 2rem;}
    .brand-title{font-size: 2.4rem;font-weight: 800;background: linear-gradient(90deg, var(--accent-1), var(--accent-2), var(--accent-3));-webkit-background-clip: text;-webkit-text-fill-color: transparent;}
    .subtitle{color:var(--muted);font-size:1.05rem;}
    .input-section, .chat-section{background:var(--card);border-radius:14px;padding:1.25rem;margin-bottom:1.25rem;box-shadow:0 10px 30px rgba(0,0,0,0.08);}
    .chat-container{height:60vh;overflow:auto;padding:0.5rem;}
    .message{display:flex;margin:0.9rem 0;animation:fadeIn .18s ease-out;}
    @keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none;}}
    .user-message{justify-content:flex-end;}
    .assistant-message{justify-content:flex-start;}
    .message-content{max-width:75%;padding:0.8rem 1rem;border-radius:12px;line-height:1.45;font-size:0.95rem;}
    .user-message .message-content{background:linear-gradient(90deg,var(--accent-1),#90e0ef);color:#012;box-shadow:0 6px 18px rgba(0,180,216,0.12);}
    .assistant-message .message-content{background:linear-gradient(90deg,#ffd6a5,var(--accent-2));color:#2b2b2b;border:1px solid rgba(0,0,0,0.03);}
    .stButton>button{background:linear-gradient(90deg,var(--accent-1),var(--accent-2));color:white;border-radius:10px;}
    @media (max-width:900px){.message-content{max-width:86%;}}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = ""

# Load API key from secrets.toml
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, google_api_key=api_key)
    st.success("✅ Connected to Gemini AI (LangChain)")
except:
    st.error("❌ Add GOOGLE_API_KEY to .streamlit/secrets.toml")
    st.stop()

def fetch_url_content(url):
    """Simple URL content fetcher"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text[:4000]  # Limit context
    except:
        return ""

# Header
st.markdown("<h1 class='brand-title'>🤖 AI Conversation Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Simple, fast chat with Gemini AI. Add URL context optionally.</p>", unsafe_allow_html=True)

# Sidebar - URL Context (optional)
with st.sidebar:
    st.markdown("### 📄 Optional Context")
    url = st.text_input("Load webpage context:", placeholder="https://example.com")
    if st.button("📥 Add Context", use_container_width=True):
        if url:
            with st.spinner("Fetching content..."):
                context = fetch_url_content(url)
                if context:
                    st.session_state.context = context
                    st.success("✅ Context loaded!")
                else:
                    st.error("❌ Failed to load URL")
        else:
            st.warning("Enter a URL")

    st.markdown("---")
    if st.button("🗑️ Clear Chat & Context"):
        st.session_state.messages = []
        st.session_state.context = ""
        st.rerun()

# Chat interface
st.markdown("<div class='chat-section'>", unsafe_allow_html=True)

chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if st.session_state.messages:
    st.markdown(f"**Context loaded:** {'Yes' if st.session_state.context else 'No'}")

st.markdown("</div>", unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response with context if available
    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            try:
                if st.session_state.context:
                    full_prompt = f"Context from webpage:\n{st.session_state.context}\n\nUser question: {prompt}\n\nAnswer using context when relevant, otherwise general knowledge."
                else:
                    full_prompt = prompt
                
                response = llm.invoke(full_prompt)
                st.markdown(response.content)
                st.session_state.messages.append({"role": "assistant", "content": response.content})
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Instructions
with st.expander("ℹ️ How to use"):
    st.markdown("""
    1. **API Key**: Already in `secrets.toml` ✅
    2. **Optional**: Add URL → "Add Context" for webpage-aware chat
    3. **Chat**: Type questions, get AI responses instantly
    4. **Easy**: No complex deps, runs smoothly!
    """)

st.markdown("---")
st.caption("Powered by Gemini 2.5 Flash via LangChain | Modern SDK")
