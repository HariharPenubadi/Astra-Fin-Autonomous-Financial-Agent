import pytest
from unittest.mock import patch, MagicMock
from src.tools import local_search_tool

@patch("src.tools.httpx.get")
def test_local_search_tool_success(mock_get):

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {
                "title": "Astra Fin Release",
                "url": "http://example.com/news",
                "content": "Astra Fin 2.0 is now live."
            }
        ]
    }
    mock_get.return_value = mock_response

    result = local_search_tool.invoke("latest news")

    assert "Astra Fin Release" in result
    assert "http://example.com/news" in result

@patch("src.tools.httpx.get")
def test_local_search_tool_no_results(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"results": []}
    mock_get.return_value = mock_response

    result = local_search_tool.invoke("weird obscure query")

    assert result == "No results found."

@patch("src.tools.httpx.get")
def test_local_search_tool_error(mock_get):
    mock_get.side_effect = Exception("Connection refused")

    result = local_search_tool.invoke("stock price")

    assert "Search Error" in result