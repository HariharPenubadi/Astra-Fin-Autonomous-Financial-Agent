from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from src.state import AgentState
from src.tools import get_tavily_tool


llm = ChatOllama(model="astra-fin", temperature=0)

def researcher(state: AgentState):
    print("RESEARCHER WORKING")
    query = state["messages"][-1]

    tavily = get_tavily_tool()
    results = tavily.invoke(query)

    if isinstance(results, list):
        content = "\n".join([r.get("content", "") for r in results])
    else:
        content = str(results)
    return {"research_data": content, "messages": [f"DATA FOUND: {content}"]}

def analyst(state: AgentState):

    print("ANALYST THINKING")
    data = state.get("research_data", "No data found.")
    prompt = f"Analyze this financial data and provide a brief summary:\n{data}"
    response = llm.invoke(prompt)
    return {"messages": [response.content]}

def critic(state: AgentState):

    print("CRITIC REVIEWING")
    last_msg = state["messages"][-1]
    if len(last_msg) < 50:
        return "rejected"
    return "approved"