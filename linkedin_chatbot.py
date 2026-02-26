import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# ------------ configuration ------------
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "AIzaSyA9ATEdHve6eze4IIY-QpowNevcxZ8w8d4")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
template = """
Use the provided context to answer the question if relevant content is available.
You can also use your general knowledge if the context doesn't fully answer it.

from PIL import Image  # Import Image from Pillow
img = Image.open("streamlit.png") # Open the image file
st.image(img, width=200) # Display the image with a specified width

Context: {context}

Question: {question}
Answer:"""
prompt = PromptTemplate.from_template(template)
# ---------------------------------------

def ingest_url(url: str):
    print(f"loading {url} …")
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
        
        # Score based on keyword matches (exact word boundaries)
        score = 0
        for word in question_words:
            if len(word) > 2:  # Skip short words
                if word in chunk_lower:
                    score += chunk_lower.count(word)
        
        scores.append((i, score, chunk))
    
    # Sort by score (descending)
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # Get top k chunks
    result = [chunk for _, _, chunk in scores[:k]]
    
    if not result:
        # If no matches, return first k chunks (fallback)
        result = chunks[:k]
    
    return result

def answer_question(question: str, chunks):
    hits = retrieve_chunks(question, chunks)
    ctx = "\n\n".join([d.page_content for d in hits])
    
    # Debug: show retrieved context preview
    print(f"[Retrieved {len(hits)} chunks]")
    
    prompt_text = prompt.format(context=ctx, question=question)
    return llm.invoke(prompt_text)

if __name__ == "__main__":
    url = input("Enter a URL: ").strip()
    try:
        chunks = ingest_url(url)
        print("\nType a question (empty line to quit).\n")
        while True:
            q = input("Q> ").strip()
            if not q:
                break
            ans = answer_question(q, chunks)
            print(f"\nA> {ans.content}\n")
    except Exception as e:
        print(f"Error: {e}")



# Create a slider to select a level between 1 and 5
level = st.slider("Choose a level", min_value=1, max_value=5)

# Display the selected level
st.write(f"Selected level: {level}")