import datetime
from langchain_ollama import ChatOllama
from src.state import AgentState
# Import the new tool
from src.tools import local_search_tool, get_retriever_tool, get_stock_data
import os

ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
llm = ChatOllama(model="astra-fin", temperature=0, base_url=ollama_url)


def researcher(state: AgentState):
    print("RESEARCHER: Routing Query")
    query = state["messages"][-1]

    # 1. Router Logic
    prompt = f"""
    You are a Senior Research Manager.
    USER QUERY: "{query}"

    INSTRUCTIONS:
    - If query asks about specific STOCKS (Apple, NVDA, Price, Invest), reply "FINANCE_TOOL: <TICKER>" (e.g., "FINANCE_TOOL: AAPL").
    - If query is greeting -> Reply "CHAT".
    - If query is internal -> Reply "INTERNAL".
    - If query is general news -> Reply "WEB".
    """
    decision = llm.invoke(prompt).content.strip()  # Remove .upper() to keep ticker case

    context = ""

    # 2. Execution Logic
    if "FINANCE_TOOL" in decision:
        # Extract ticker from "FINANCE_TOOL: AAPL"
        ticker = decision.split(":")[-1].strip()
        print(f"   (Route: YAHOO FINANCE - {ticker})")
        context = get_stock_data.invoke(ticker)

    elif "INTERNAL" in decision:
        print("   (Route: INTERNAL DATABASE)")
        context = get_retriever_tool(query)

    elif "WEB" in decision:
        print("   (Route: PUBLIC WEB)")
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        context = local_search_tool.invoke(f"{query} {today}")

    else:
        print("   (Route: CHAT)")
        context = "FLAG_CHAT_INTERACTION"

    return {"research_data": context, "messages": [f"DATA_INCOMING"]}


def analyst(state: AgentState):
    print("ANALYST: Generating Report")
    data = state.get("research_data", "")
    query = state["messages"][0]

    if "FLAG_CHAT_INTERACTION" in data:
        # Simple Chat Mode
        prompt = f"User said: '{query}'. Be helpful and brief."
    else:
        # PRO ANALYST MODE
        prompt = f"""
        You are a Wall Street Investment Analyst. 

        USER QUESTION: "{query}"
        OFFICIAL MARKET DATA: 
        {data}

        INSTRUCTIONS:
        1. **The Numbers:** State the Current Price and the Target High Price explicitly.
        2. **The Verdict:** Answer the user's question ("Can I invest?"). 
           - Compare Current Price vs Target High (Is there upside?).
           - Mention the Analyst Recommendation (Buy/Hold/Sell).
        3. **Risk:** Mention the P/E Ratio (Is it expensive?).

        TONE:
        - Confident, Data-Driven, Professional.
        - NO Markdown tables, just clear paragraphs and bullet points.
        """

    response = llm.invoke(prompt)
    return {"messages": [response.content]}


# Critic remains the same
def critic(state: AgentState):
    if "FLAG_CHAT_INTERACTION" in state.get("research_data", ""): return "approved"
    if len(state["messages"][-1]) < 10: return "rejected"
    return "approved"