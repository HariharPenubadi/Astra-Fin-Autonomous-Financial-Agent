from langgraph.graph import StateGraph
from src.graph.state import AstraState

from src.agents.planner import planner
from src.agents.finance_agent import finance_agent
from src.profile.investor_profile import investor_profile
from src.advisory.advisor import advisor
from src.agents.reasoner import reasoner
from src.agents.critic import critic


def route_after_planner(state):
    intent = state["intent"]

    if intent == "finance_fact":
        return "finance_agent"

    elif intent in {"investment_setup", "investment_advice"}:
        return "investor_profile"

    else:
        return "reasoner"


def build_graph():
    graph = StateGraph(AstraState)

    graph.add_node("planner", planner)
    graph.add_node("finance_agent", finance_agent)
    graph.add_node("investor_profile", investor_profile)
    graph.add_node("advisor", advisor)
    graph.add_node("reasoner", reasoner)
    graph.add_node("critic", critic)

    graph.set_entry_point("planner")

    graph.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "finance_agent": "finance_agent",
            "investor_profile": "investor_profile",
            "reasoner": "reasoner"
        }
    )

    graph.add_edge("finance_agent", "critic")

    graph.add_edge("investor_profile", "advisor")

    graph.add_edge("advisor", "critic")

    graph.add_edge("reasoner", "critic")

    return graph.compile()