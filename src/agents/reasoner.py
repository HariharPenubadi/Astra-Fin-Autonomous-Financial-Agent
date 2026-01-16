from src.memory.episodic import recall_episodes
from src.retrieval.hybrid import hybrid_retrieve
from src.core.llm import get_llm


def reasoner(state):
    intent = state["intent"]
    query = state["query"]
    llm = get_llm()

    if intent == "greeting":
        return {"answer": "Hello! I am ASTRA, your personal financial intelligence. How can I assist you today?"}

    if intent == "identity":
        return {
            "answer": "I am **ASTRA**, a hyper-personalized financial AI agent. I can track markets, analyze stocks, and build investment portfolios for you."}

    if intent == "memory_question":
        history = recall_episodes(3)
        if not history:
            return {"answer": "We haven't discussed much yet."}

        answer = "Here is what we discussed recently:\n"
        for row in history:
            answer += f"- You asked: {row[0]}\n"
        return {"answer": answer}

    retrieval = hybrid_retrieve(state)
    context_docs = retrieval["vector_results"] + retrieval["web_results"]

    context_str = "\n".join([str(d) for d in context_docs])

    if not context_str:
        return {
            "answer": "I don't have specific data on that, but I can help you with investment planning or market data."}

    rag_answer = llm.invoke(
        f"Answer the user query based on this context:\n{context_str}\n\nQuery: {query}"
    ).content

    return {"answer": rag_answer}