from langchain_ollama import ChatOllama
from src.core.config import settings

def get_llm():
    return ChatOllama(
        model=settings.MODEL_NAME,
        temperature=0.2,
        num_ctx=8192
    )
