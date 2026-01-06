from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.agents import researcher, analyst, critic
from dotenv import load_dotenv

load_dotenv()

def build_graph():

    workflow = StateGraph(AgentState)

    workflow.add_node("researcher", researcher)
    workflow.add_node("analyst", analyst)

    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "analyst")

    def check_quality(state):
        result = critic(state)
        if result == "approved" or state.get("revision_count", 0) > 2:
            return END
        else:
            return "researcher"

    workflow.add_conditional_edges("analyst", check_quality)
    return workflow.compile()

if __name__ == "__main__":
    app = build_graph()

    print("Initailizing Astra Fin")
    user_input = "What is the latest stock price for Apple (AAPL)?"

    result = app.invoke({
        "messages": [user_input],
        "revision_count": 0
    })

    print("\n--- FINAL OUTPUT ---")
    print(result["messages"][-1])