import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient


def get_tavily_tool():
    return TavilySearchResults(max_results=3)


def get_retriever_tool(query: str):
    print(f"(Vector Search for: '{query}')")

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    url = os.getenv("QDRANT_URL", "http://qdrant:6333")

    try:
        client = QdrantClient(url=url, prefer_grpc=False)

        vector_store = QdrantVectorStore(
            client=client,
            collection_name="internal_financial_docs",
            embedding=embeddings,
        )

        docs = vector_store.similarity_search(query, k=1)

        if not docs:
            return "No internal records found."

        return "\n\n".join([d.page_content for d in docs])

    except Exception as e:
        print(f"Database Error: {str(e)}")
        return f"Database Error: Could not retrieve documents due to {str(e)}"