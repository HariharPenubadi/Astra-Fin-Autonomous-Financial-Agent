import httpx
from src.core.config import settings

def web_retrieve(query: str):
    if "revenue" in query.lower():
        query = f"{query} site:apple.com OR site:sec.gov OR site:wikipedia.org"

    response = httpx.get(
        f"{settings.SEARXNG_URL}/search",
        params={"q": query, "format": "json"},
        timeout=3.0
    )

    return response.json().get("results", [])

