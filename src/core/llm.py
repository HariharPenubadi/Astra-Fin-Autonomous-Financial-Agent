from langchain_ollama import ChatOllama
from src.core.config import settings


def get_llm():
    print(f"Connecting to Ollama at: {settings.OLLAMA_BASE_URL}")

    return ChatOllama(
        model=settings.MODEL_NAME,
        temperature=0,
        base_url=settings.OLLAMA_BASE_URL,
        keep_alive="5m"
    )