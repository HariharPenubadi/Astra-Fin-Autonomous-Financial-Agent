import pytest
from src.agents.planner import planner
from src.profile.investor_profile import investor_profile
from src.advisory.advisor import advisor
from src.memory.short_term import clear


@pytest.fixture(autouse=True)
def clean_memory():
    clear()


def test_planner_routing():
    test_cases = [
        ("I have 5000 dollars", "investment_setup"),
        ("Where should I invest?", "investment_advice"),
        ("Apple revenue 2023", "finance_fact"),
        ("Hello ASTRA", "greeting"),
        ("Who are you?", "identity"),
    ]

    for query, expected_intent in test_cases:
        state = {"query": query}
        result = planner(state)
        assert result["intent"] == expected_intent, f"Failed on '{query}'"


def test_profile_extraction_inr():
    state = {"query": "I have 50000 rupees for investment"}
    updated_state = investor_profile(state)

    profile = updated_state["investor_profile"]
    assert profile["budget"] == 50000
    assert profile["currency"] == "INR"


def test_profile_extraction_usd_risk():
    state = {"query": "I have $2000 and I want high risk"}
    updated_state = investor_profile(state)

    profile = updated_state["investor_profile"]
    assert profile["budget"] == 2000
    assert profile["currency"] == "USD"
    assert profile["risk"] == "high"


def test_advisor_logic_sanity():
    state = {
        "query": "Where to invest?",
        "investor_profile": {
            "budget": 10000,
            "currency": "INR",
            "risk": "low",
            "horizon": "long",
            "market": "both"
        }
    }

    result = advisor(state)
    answer = result["answer"].lower()

    assert "debt" in answer
    assert "equity" in answer
    assert "fd" in answer or "liquid" in answer


def test_advisor_knowledge_injection():
    state = {
        "query": "Give me specific names",
        "investor_profile": {
            "budget": 5000,
            "currency": "INR",
            "risk": "high",
            "horizon": "long"
        }
    }

    result = advisor(state)
    answer = result["answer"].lower()

    assert "small cap" in answer or "flexi cap" in answer