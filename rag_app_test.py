import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

# Set your Google API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA9ATEdHve6eze4IIY-QpowNevcxZ8w8d4"

# INGESTION
print("Loading document...")
loader = TextLoader("company_policy.txt")
docs = loader.load()

# CHUNKING
print("Splitting text...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(docs)

# EMBEDDING & VECTOR DB
print("Creating embeddings and Vector DB...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = FAISS.from_documents(chunks, embeddings)

# RETRIEVAL
question = "What are the company's leave policies?"
print(f"\nSearching for: {question}")
retriever = vector_db.as_retriever(search_kwargs={"k": 2})
relevant_chunks = retriever.invoke(question)

# GENERATION
print("\nGenerating Answer...")
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

# The RAG Prompt
template = """
Use the following pieces of context to answer the question. 
If you don't know the answer, just say that you don't know.

Context: {context}

Question: {question}
Answer:"""

prompt = PromptTemplate.from_template(template)

# Format the context and send it
context_text = "\n\n".join([doc.page_content for doc in relevant_chunks])
final_prompt = prompt.format(context=context_text, question=question)

answer = llm.invoke(final_prompt)
print(f"\nAI Answer:\n{answer.content}")
