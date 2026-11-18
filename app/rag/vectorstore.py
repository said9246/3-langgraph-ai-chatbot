from langchain_community.vectorstores import FAISS
from app.rag.embeddings import embeddings

def create_vectorstore(chunks):
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    return vectorstore