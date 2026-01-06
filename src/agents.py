from langchain_ollama import ChatOllama
from src.state import AgentState
from src.tools import get_tavily_tool, get_retriever_tool

llm = ChatOllama(model="astra-fin", temperature=0)


def researcher(state: AgentState):

    print("RESEARCHER: Routing Query")
    query = state["messages"][-1]
    prompt = f"""
    You are a strict Data Router.

    QUERY: "{query}"

    INSTRUCTIONS:
    1. If the query contains the words "internal", "memo", "confidential", or "private", you MUST reply with "INTERNAL".
    2. Do NOT use your general knowledge.
    3. For everything else, reply with "WEB".

    Reply ONLY with the word "INTERNAL" or "WEB".
    """
    decision = llm.invoke(prompt).content.strip().upper()

    if "INTERNAL" in decision:
        print("Route: INTERNAL DATABASE")
        context = get_retriever_tool(query)
    else:
        print("Route: PUBLIC WEB")
        tavily = get_tavily_tool()
        results = tavily.invoke(query)
        context = "\n".join([r["content"] for r in results]) if isinstance(results, list) else str(results)

    return {"research_data": context, "messages": [f"DATA ({decision}): {context}"]}

def analyst(state: AgentState):
    print("ANALYST THINKING")
    data = state.get("research_data", "")
    prompt = f"Analyze this data and answer the user's question:\n{data}"
    response = llm.invoke(prompt)
    return {"messages": [response.content]}

def critic(state: AgentState):
    print("CRITIC REVIEWING")
    if len(state["messages"][-1]) < 20: return "rejected"
    return "approved"