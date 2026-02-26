# linkedin_chatbot.py
import os
from langchain_community.document_loaders import WebBaseLoader        # pip install langchain-community
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS                   # pip install langchain-community
from langchain_huggingface import HuggingFaceEmbeddings            # pip install langchain-huggingface
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# ------------ configuration ------------
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "<your key>")

llm = ChatGoogleGenerativeAI(model="gemini‑2.5‑flash", temperature=0.7)
template = """
Use the following pieces of context to answer the question.
If you don't know the answer, just say that you don't know.

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

def build_retriever(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(chunks, embeddings)
    return db.as_retriever(search_kwargs={"k": 3})

def answer_question(question: str, retriever):
    hits = retriever.invoke(question)
    ctx = "\n\n".join([d.page_content for d in hits])
    prompt_text = prompt.format(context=ctx, question=question)
    return llm.invoke(prompt_text)

if __name__ == "__main__":
    url = input("Enter a LinkedIn (or other) URL: ").strip()
    chunks = ingest_url(url)
    retriever = build_retriever(chunks)

    print("\nType a question (empty line to quit).\n")
    while True:
        q = input("Q> ").strip()
        if not q:
            break
        ans = answer_question(q, retriever)
        print("\nA> ", ans, "\n")