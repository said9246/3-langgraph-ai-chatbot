from app.rag.loader import load_pdf
from app.rag.splitter import split_documents
from app.rag.vectorstore import create_vectorstore
from app.rag.retriever import create_retriever
from app.rag.chain import create_rag_chain


def initialize_rag(pdf_path):
    documents = load_pdf(pdf_path)
    chunks = split_documents(documents)
    vectorstore = create_vectorstore(chunks)
    retriever = create_retriever(vectorstore)
    rag_chain = create_rag_chain(retriever)

    return rag_chain