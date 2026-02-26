import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

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

# SIMPLE RETRIEVAL (keyword-based, no embeddings)
question = "What are the company's leave policies?"
print(f"\nSearching for: {question}")

# Basic keyword search
relevant_chunks = []
keywords = ["leave", "policy", "vacation", "sick", "maternity", "paternity"]
for chunk in chunks:
    if any(keyword in chunk.page_content.lower() for keyword in keywords):
        relevant_chunks.append(chunk)

if not relevant_chunks:
    relevant_chunks = chunks[:2]  # Fallback to first chunks

# GENERATION
print("\nGenerating Answer...")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

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
