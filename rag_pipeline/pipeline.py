from rag_pipeline.loader import load_documents
from rag_pipeline.splitter import split_documents
from rag_pipeline.vector_store import build_vectorstore, load_vectorstore
from rag_pipeline.retriever import get_retriever

def ingest_pipeline(data_dir: str):
    documents = load_documents(data_dir)
    chunks = split_documents(documents)
    build_vectorstore(chunks)
    print(f"✅ Ingested {len(chunks)} chunks")

def query_pipeline():
    vectorstore = load_vectorstore()
    if not vectorstore:
        raise RuntimeError("Vector DB not found. Run ingestion first.")

    return get_retriever(vectorstore)
