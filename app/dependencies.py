from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from app.config import MODEL_NAME, EMBED_MODEL_NAME, TEMPERATURE, DIMENSIONS


def llm():
    """Initialized the Chat Model"""
    return ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)


def embed_model():
    """Initialed the Embedding Model"""
    return OpenAIEmbeddings(model=EMBED_MODEL_NAME, dimensions=DIMENSIONS)
