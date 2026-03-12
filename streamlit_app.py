import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
from bs4 import BeautifulSoup
import os

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
<style>
:root{--bg-1:#ffecd2;--bg-2:#fcb69f;--card:rgba(255,255,255,0.9);--muted:#5b5b6b;--accent-1:#00b4d8;--accent-2:#ff6b6b;}
*{box-sizing:border-box;font-family:'Inter',sans-serif;}
body{background:linear-gradient(135deg,var(--bg-1),var(--bg-2));}
.stApp{padding:2rem;}
.brand-title{font-size:2.4rem;font-weight:800;background:linear-gradient(90deg,var(--accent-1),var(--accent-2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.chat-section{background:var(--card);border-radius:14px;padding:1.25rem;box-shadow:0 10px 30px rgba(0,0,0,0.08);}
.user .message-content{background:linear-gradient(90deg,var(--accent-1),#90e0ef);color:#012;}
.assistant .message-content{background:linear-gradient(90deg,#ffd6a5,var(--accent-2));color:#2b2b2b;}
.stButton>button{background:linear-gradient(90deg,var(--accent-1),var(--accent-2));color:white;border-radius:10px;}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = ""

# LLM - User specified
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    st.success("Connected to Gemini 2.5 Flash")
except Exception as e:
    st.error(f"Setup error: {e}")
    st.stop()

def get_url_text(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        lines = (line.strip() for line in soup.get_text().splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        return text[:5000]
    except Exception as e:
        return f"Load error: {str(e)}"

st.markdown("<h1 class='brand-title'>🤖 Gemini Chatbot</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### URL Context")
    url = st.text_input("Enter URL")
    if st.button("Load", use_container_width=True):
        if url:
            with st.spinner("Loading..."):
                text = get_url_text(url)
                st.session_state.context = text if not text.startswith("Load error") else ""
                if st.session_state.context:
                    st.success("Context loaded!")
                else:
                    st.error(text)
        else:
            st.warning("Enter URL")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.context = ""
        st.rerun()

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.context:
    with st.expander("Context preview"):
        st.text_area("", st.session_state.context[:1000], disabled=True, height=100)

# Input
prompt = st.chat_input("Ask...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                full_prompt = prompt
                if st.session_state.context:
                    full_prompt = f"Context:\n{st.session_state.context}\n\nUser: {prompt}\n\nConcise answer:"
                response = llm.invoke(full_prompt)
                msg = response.content
                st.markdown(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            except Exception as e:
                st.error(f"Response error: {str(e)}")

with st.expander("Setup"):
    st.markdown("""
- **Secrets**: GOOGLE_API_KEY
- **Local**: streamlit run streamlit_app.py
- **Cloud**: Push to GitHub → Streamlit Cloud
    """)

st.caption("Gemini 2.5 Flash - Works everywhere")
