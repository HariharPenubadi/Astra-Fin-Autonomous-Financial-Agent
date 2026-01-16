import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MODEL_NAME = os.getenv("MODEL_NAME", "astra-fin:latest")
    EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-base-en-v1.5")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8080")

    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

settings = Settings()