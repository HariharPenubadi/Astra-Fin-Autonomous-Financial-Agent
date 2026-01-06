from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain_ollama import OllamaEmbeddings
import os

qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
print(f"Connecting to Qdrant at: {qdrant_url}")

client = QdrantClient(url=qdrant_url, prefer_grpc=False)
embeddings = OllamaEmbeddings(model="nomic-embed-text")
collection_name = "internal_financial_docs"

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
)

documents = [
    "Internal Memo: Project Titan is delayed until Q4 2026. This is confidential.",
    "Analyst Note: We believe Tesla (TSLA) is undervalued due to upcoming robotics breakthrough.",
    "Risk Report: The primary risk for NVIDIA is chip supply chain instability in Taiwan."
]

print("Embedding documents...")
points = []

for idx, doc in enumerate(documents):
    vector = embeddings.embed_query(doc)
    points.append(models.PointStruct(id=idx, vector=vector, payload={"page_content": doc}))

client.upsert(collection_name=collection_name, points=points)
print(f"SUCCESS: Uploaded {len(documents)} secret documents")