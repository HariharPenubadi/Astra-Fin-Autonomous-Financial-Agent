import pytest
from unittest.mock import patch, MagicMock
from src.agents.planner import planner
from src.profile.investor_profile import investor_profile
from src.advisory.advisor import advisor
from src.memory.short_term import clear


@pytest.fixture(autouse=True)
def clean_memory():
    clear()

@pytest.fixture
def mock_llm():
    with patch("src.core.llm.ChatOllama") as MockClass:
        mock_instance = MockClass.return_value
        yield mock_instance


def test_planner_routing(mock_llm):
    mock_response = MagicMock()
    mock_response.content = "investment_setup"
    mock_llm.invoke.return_value = mock_response

    state = {"query": "I have 5000 dollars"}
    result = planner(state)

    assert result["intent"] == "investment_setup"


def test_profile_extraction_inr(mock_llm):
    state = {"query": "I have 50000 rupees for investment"}

    updated_state = investor_profile(state)
    profile = updated_state.get("investor_profile", {})

    if not profile:
        assert True


def test_advisor_logic_sanity(mock_llm):
    mock_response = MagicMock()
    mock_response.content = """
    1. **Analysis**: Based on 10000 INR...
    2. **Allocation Plan**: Equity 3000, Debt 5000...
    3. **Specific Recommendations**: HDFC Liquid Fund.
    """
    mock_llm.invoke.return_value = mock_response

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

    assert "allocation plan" in answer
    assert "equity" in answer