from pathlib import Path
from langchain_community.vectorstores import FAISS
from rag_pipeline.embedding import get_embedding_function

VECTOR_DIR = Path("vector_db")

def load_vectorstore():
    if not VECTOR_DIR.exists():
        return None

    return FAISS.load_local(
        VECTOR_DIR,
        get_embedding_function(),
        allow_dangerous_deserialization=True,
    )

def build_vectorstore(chunks):
    embeddings = get_embedding_function()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTOR_DIR)
    return vectorstore
