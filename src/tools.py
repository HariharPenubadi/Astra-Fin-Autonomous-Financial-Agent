from langchain_community.tools.tavily_search import TavilySearchResults
import os

def get_tavily_tool():

    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY not found in environment variables")

    return TavilySearchResults(max_results=3)