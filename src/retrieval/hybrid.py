from src.retrieval.vector import vector_retrieve
from src.retrieval.web import web_retrieve

def hybrid_retrieve(state):
    query = state["query"]

    vector_results = vector_retrieve(query)

    web_results = []
    if not state.get("disable_web"):
        web_results = web_retrieve(query)

    return {
        "vector_results": vector_results,
        "web_results": web_results
    }

