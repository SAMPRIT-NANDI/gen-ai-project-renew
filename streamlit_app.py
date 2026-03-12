import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = ""

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

def get_url_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)[:5000]
        return text
    except Exception as e:
        return str(e)

st.title("🤖 Gemini Chatbot")

with st.sidebar:
    url = st.text_input("URL")
    if st.button("Load Context"):
        text = get_url_text(url)
        st.session_state.context = text
        st.success("Loaded" if len(text) > 10 else "Error")

# Chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

prompt = st.chat_input("Ask...", key="chat")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    
    with st.chat_message("assistant"):
        full_prompt = prompt
        if st.session_state.context:
            full_prompt = f"Context: {st.session_state.context}\n\n{prompt}"
        response = llm.invoke(full_prompt)
        st.markdown(response.content)
        st.session_state.messages.append({"role": "assistant", "content": response.content})

if st.session_state.context:
    with st.expander("Context"):
        st.text(st.session_state.context[:1000])

st.caption("Deploy-ready")
