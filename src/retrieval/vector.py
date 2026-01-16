from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from langchain_qdrant import QdrantVectorStore
from src.core.embeddings import get_embeddings
from src.core.config import settings


COLLECTION_NAME = "astra_docs"


def get_client():
    return QdrantClient(url=settings.QDRANT_URL)


def ensure_collection(client):
    collections = client.get_collections().collections
    existing = [c.name for c in collections]

    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE,
            ),
        )


def get_vector_store():
    client = get_client()
    ensure_collection(client)

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=get_embeddings(),
    )


def vector_retrieve(query: str, k: int = 5):
    store = get_vector_store()
    return store.similarity_search(query, k=k)
