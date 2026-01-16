from typing import TypedDict, List, Any

class AstraState(TypedDict, total=False):
    query: str
    intent: str
    plan: str
    context: str
    vector_results: list
    web_results: list
    answer: str
    review: str
    memory_locked: bool


