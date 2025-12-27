from langchain_community.vectorstores import FAISS
from rag_pipeline.embedding import get_embedding_function
import os


def build_vectorstore(chunks, persist_directory="vector_db"):
    if not chunks:
        raise ValueError("No chunks provided to build vectorDB")
    embeddings = get_embedding_function()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(persist_directory)
    return vectorstore


def load_vectorstore(persist_directory="vector_db"):
    return FAISS.load_local(
        persist_directory,
        embeddings=get_embedding_function(),
        allow_dangerous_deserialization=True,
    )
