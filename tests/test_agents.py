import pytest
from unittest.mock import MagicMock, patch
from src.state import AgentState
from src.agents import critic

def test_critic_approval():
    mock_state = {
        "messages": ["This is a very long and detailed financial analysis report that definitely meets the length requirement."],
        "research_data": "",
        "revision_count": 0
    }
    result = critic(mock_state)
    assert result == "approved"

def test_critic_rejection():
    mock_state = {
        "messages": ["Too short."],
        "research_data": "",
        "revision_count": 0
    }
    result = critic(mock_state)
    assert result == "rejected"