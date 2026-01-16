import os
from dotenv import load_dotenv
os.environ["LANGCHAIN_TRACING_V2"] = "false"
load_dotenv()

class Settings:
    QDRANT_URL = os.getenv("QDRANT_URL")
    SEARXNG_URL = os.getenv("SEARXNG_URL")
    MODEL_NAME = "astra-fin:latest"
    EMBED_MODEL = "BAAI/bge-base-en-v1.5"

settings = Settings()
