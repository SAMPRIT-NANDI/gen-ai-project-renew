import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from groq import Groq
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = ""
if "llm_choice" not in st.session_state:
    st.session_state.llm_choice = "Gemini"

# Initialize clients
def get_gemini_client():
    api_key = st.secrets.get("GOOGLE_API_KEY", "")
    if not api_key:
        st.error("Please set GOOGLE_API_KEY in .streamlit/secrets.toml")
        st.stop()
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        google_api_key=api_key
    )

def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("Please set GROQ_API_KEY in .streamlit/secrets.toml")
        st.stop()
    return Groq(
        api_key=api_key
    )

def get_url_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)[:5000]
        return text
    except Exception as e:
        return str(e)

st.title("🤖 AI Chat Assistant")

st.info("💡 Tip: Get your free API keys from:\n- Google Gemini: https://aistudio.google.com/\n- Groq: https://console.groq.com/\nThen add them to `.streamlit/secrets.toml`!")

with st.sidebar:
    st.header("Settings")
    
    # LLM Choice
    st.session_state.llm_choice = st.radio(
        "Choose LLM",
        ["Gemini", "Groq (Llama 3.1)"],
        index=0
    )
    
    # URL Context
    st.subheader("Add Context from URL")
    url = st.text_input("Enter URL")
    if st.button("Load Context"):
        text = get_url_text(url)
        st.session_state.context = text
        if len(text) > 10:
            st.success("✅ Context loaded successfully!")
        else:
            st.error("❌ Failed to load context")
    
    # Clear Context
    if st.session_state.context and st.button("Clear Context"):
        st.session_state.context = ""
        st.success("✅ Context cleared")
    
    # Clear Chat
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.success("✅ Chat cleared")

# Chat interface
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

prompt = st.chat_input("Ask anything...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                full_prompt = prompt
                if st.session_state.context:
                    full_prompt = f"Use the following context to answer the question. If you don't know the answer, just say you don't know.\n\nContext: {st.session_state.context}\n\nQuestion: {prompt}"
                
                if st.session_state.llm_choice == "Gemini":
                    llm = get_gemini_client()
                    response = llm.invoke(full_prompt)
                    answer = response.content
                else:  # Groq
                    client = get_groq_client()
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a helpful AI assistant."
                            },
                            {
                                "role": "user",
                                "content": full_prompt
                            }
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.7
                    )
                    answer = chat_completion.choices[0].message.content
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Display context
if st.session_state.context:
    with st.expander("📄 View Loaded Context"):
        st.text(st.session_state.context[:2000])

st.caption("🚀 Built with Streamlit, Gemini, Groq, and BeautifulSoup - Perfect for your resume!")
