from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from app.config import MODEL_NAME, EMBED_MODEL_NAME, TEMPERATURE, DIMENSIONS, CHUNK_SIZE

_rag_pipeline = None


def llm():
    """Initialized the Chat Model"""
    return ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)


def embed_model():
    """Initialed the Embedding Model"""
    return OpenAIEmbeddings(
        model=EMBED_MODEL_NAME, dimensions=DIMENSIONS, chunk_size=CHUNK_SIZE
    )


def get_rag_pipeline():
    from rag_pipeline.pipeline import RAGPipeline

    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline()
        _rag_pipeline.load()
    return _rag_pipeline
