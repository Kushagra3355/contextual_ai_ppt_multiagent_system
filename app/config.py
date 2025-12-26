from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME", "text-embedding-3-small")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0))
DIMENSIONS = float(os.getenv("DIMENSIONS", 128))

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing")