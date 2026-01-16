import os
import httpx
import yfinance as yf  # <--- Import this
from langchain_core.tools import tool
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient


# --- NEW: PROFESSIONAL STOCK TOOL ---
@tool("stock_data_tool")
def get_stock_data(ticker: str):
    """
    Get real-time stock data, fundamentals, and analyst recommendations.
    Input should be a ticker symbol (e.g., AAPL, NVDA, TSLA).
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Extract key metrics for a "High Return" analysis
        price = info.get('currentPrice', 'N/A')
        target_high = info.get('targetHighPrice', 'N/A')
        recommendation = info.get('recommendationKey', 'N/A')  # e.g., 'buy'
        pe_ratio = info.get('trailingPE', 'N/A')

        return f"""
        [REAL-TIME MARKET DATA]
        Ticker: {ticker.upper()}
        Current Price: ${price}
        Analyst Recommendation: {recommendation.upper()}
        Target High Price (Upside Potential): ${target_high}
        P/E Ratio: {pe_ratio}
        52-Week High: ${info.get('fiftyTwoWeekHigh')}
        """
    except Exception as e:
        return f"Error fetching stock data: {str(e)}"
@tool(
    description="Performs a live web search using the local SearXNG engine. Use this for external news, stock prices, or recent events.")
def local_search_tool(query: str):
    # (Docstring is still good practice, but no longer required for the crash fix)
    """
    Performs a live web search using the local SearXNG engine.
    """
    url = os.getenv("SEARXNG_URL", "http://searxng:8080")

    try:
        response = httpx.get(
            f"{url}/search",
            params={
                "q": query,
                "format": "json",
                "categories": "general,news"
            },
            timeout=5.0
        )

        # Check if the request was actually successful
        if response.status_code != 200:
            return f"Search failed with status {response.status_code}"

        results = response.json()

        parsed_results = []
        if "results" in results:
            for r in results["results"][:3]:
                title = r.get('title', 'No Title')
                link = r.get('url', 'No Link')
                content = r.get('content', 'No Content')
                parsed_results.append(f"Title: {title}\nLink: {link}\nSnippet: {content}")

        return "\n\n".join(parsed_results) if parsed_results else "No results found."

    except Exception as e:
        return f"Search Error: {str(e)}"


def get_retriever_tool(query: str):
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # Pass explicit URL to embeddings
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=ollama_url  # <--- CRITICAL ADDITION
    )

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
        return f"Database Error: {str(e)}"