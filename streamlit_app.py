import streamlit as st
import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure page
st.set_page_config(
    page_title="URL Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful dark theme
st.markdown("""
    <style>
    :root{
        --bg-1: #ffecd2; /* warm cream */
        --bg-2: #fcb69f; /* coral */
        --card: rgba(255,255,255,0.9);
        --muted: #5b5b6b;
        --accent-1: #00b4d8; /* teal */
        --accent-2: #ff6b6b; /* pink */
        --accent-3: #ffd166; /* yellow */
    }

    *{box-sizing: border-box;font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial}

    body {
        margin:0;
        padding:0;
        background: linear-gradient(135deg, var(--bg-1) 0%, var(--bg-2) 100%);
    }

    .stApp > div:first-child {
        padding: 2rem 2rem 4rem 2rem;
    }

    .brand-title{
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, var(--accent-1), var(--accent-2), var(--accent-3));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }

    .subtitle{color:var(--muted);margin-bottom:1.6rem;font-size:1.05rem}

    .input-section, .chat-section{background:var(--card);border-radius:14px;padding:1.25rem;margin-bottom:1.25rem;box-shadow:0 10px 30px rgba(0,0,0,0.08)}

    .chat-container{height:56vh;min-height:300px;overflow:auto;padding:0.5rem}

    .message{display:flex;margin:0.9rem 0;animation:fadeIn .18s ease-out}
    @keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}

    .user-message{justify-content:flex-end}
    .assistant-message{justify-content:flex-start}

    .message-content{max-width:72%;padding:0.8rem 1rem;border-radius:12px;line-height:1.45;font-size:0.95rem}

    .user-message .message-content{background:linear-gradient(90deg,var(--accent-1),#90e0ef);color:#012;box-shadow:0 6px 18px rgba(0,180,216,0.12)}
    .assistant-message .message-content{background:linear-gradient(90deg,#ffd6a5,var(--accent-2));color:#2b2b2b;border:1px solid rgba(0,0,0,0.03)}

    .status-badge{display:inline-block;padding:0.45rem 0.9rem;border-radius:999px;background:linear-gradient(90deg,var(--accent-1),var(--accent-2));color:white;font-weight:600}

    .stTextInput>div>div>input{background:transparent;border:1px solid rgba(0,0,0,0.06);padding:0.6rem 0.9rem;border-radius:8px}

    .stButton>button{background:linear-gradient(90deg,var(--accent-1),var(--accent-2));color:white;border-radius:10px;padding:0.6rem 1rem}

    .context-preview{font-size:0.9rem;color:var(--muted);margin-top:0.5rem;padding:0.75rem;background:rgba(0,0,0,0.03);border-radius:8px}

    /* responsive tweaks */
    @media (max-width:900px){.message-content{max-width:86%}.stApp>div:first-child{padding:1rem}}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chunks" not in st.session_state:
    st.session_state.chunks = None
if "url_loaded" not in st.session_state:
    st.session_state.url_loaded = False

# Configure API
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

template = """
Use the provided context to answer the question if relevant content is available.
You can also use your general knowledge if the context doesn't fully answer it.

Context: {context}

Question: {question}
Answer:"""
prompt = PromptTemplate.from_template(template)

# Helper functions
def ingest_url(url: str):
    """Load and split document from URL"""
    loader = WebBaseLoader(url)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)

def retrieve_chunks(question: str, chunks, k: int = 3):
    """Smart retrieval with scoring"""
    question_lower = question.lower()
    question_words = set(question_lower.split())
    
    scores = []
    for i, chunk in enumerate(chunks):
        chunk_lower = chunk.page_content.lower()
        score = 0
        for word in question_words:
            if len(word) > 2:
                if word in chunk_lower:
                    score += chunk_lower.count(word)
        scores.append((i, score, chunk))
    
    scores.sort(key=lambda x: x[1], reverse=True)
    result = [chunk for _, _, chunk in scores[:k]]
    
    if not result:
        result = chunks[:k]
    
    return result

def answer_question(question: str, chunks):
    """Generate answer from chunks"""
    hits = retrieve_chunks(question, chunks)
    ctx = "\n\n".join([d.page_content for d in hits])
    prompt_text = prompt.format(context=ctx, question=question)
    return llm.invoke(prompt_text).content

# Header
st.markdown("<h1>🤖 URL Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Ask questions about any webpage content using AI</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h2>Settings</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # URL Input
    st.markdown("<h3>Load Content</h3>", unsafe_allow_html=True)
    url = st.text_input(
        "Enter a URL:",
        placeholder="https://example.com",
        label_visibility="collapsed"
    )
    
    if st.button("📥 Load URL", use_container_width=True):
        if url.strip():
            try:
                with st.spinner("Loading and processing URL..."):
                    st.session_state.chunks = ingest_url(url)
                    st.session_state.url_loaded = True
                    st.session_state.messages = []
                    st.success(f"✅ Successfully loaded {len(st.session_state.chunks)} chunks!")
            except Exception as e:
                st.error(f"❌ Error loading URL: {str(e)}")
        else:
            st.warning("⚠️ Please enter a valid URL")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
    
    # Info
    st.markdown("---")
    st.markdown("<h3>ℹ️ How it works</h3>", unsafe_allow_html=True)
    st.info("""
    1. Paste a URL in the text box
    2. Click "Load URL" to fetch content
    3. Ask questions about the page
    4. AI will answer based on content + knowledge
    """)

# Main content area
if st.session_state.url_loaded and st.session_state.chunks:
    st.markdown("<div class='status-badge'>✅ Content Loaded - Ready to chat</div>", unsafe_allow_html=True)
    
    # Chat display
    st.markdown("<div class='chat-section'>", unsafe_allow_html=True)
    
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.messages:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(
                        f"""
                        <div class='message user-message'>
                            <div class='message-content'>{msg['content']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class='message assistant-message'>
                            <div class='message-content'>{msg['content']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.markdown(
                """
                <div style='text-align: center; padding: 3rem; color: #a0a0b0;'>
                    <p style='font-size: 1.2rem; margin-bottom: 1rem;'>👋 Start the conversation</p>
                    <p>Ask any question about the loaded content</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Input area
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        user_input = st.text_input(
            "Your question:",
            placeholder="What is this page about?",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", use_container_width=True)
    
    if send_button and user_input.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get AI response
        with st.spinner("Thinking..."):
            try:
                response = answer_question(user_input, st.session_state.chunks)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Error: {str(e)}"
                })
        
        st.rerun()

else:
    # Welcome screen
    st.markdown("""
    <div style='text-align: center; padding: 4rem 2rem;'>
        <h2 style='color: #a0a0b0; margin-bottom: 2rem;'>👈 Get Started</h2>
        <p style='color: #a0a0b0; font-size: 1.1rem; line-height: 1.8;'>
            Enter a URL in the sidebar to begin chatting with the AI about that page's content.
        </p>
        <p style='color: #707080; margin-top: 2rem; font-size: 0.9rem;'>
            Works with any public webpage (Wikipedia, News, Blogs, etc.)
        </p>
    </div>
    """, unsafe_allow_html=True)
