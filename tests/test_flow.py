from src.graph.astra_graph import build_graph


def test_full_conversation_flow():
    graph = build_graph()

    inputs = {"query": "I have 10000 rupees and I prefer low risk"}
    result = graph.invoke(inputs)

    assert "answer" in result
    response = result["answer"].lower()

    assert "10000" in response or "10,000" in response
    assert "debt" in response

    inputs_2 = {"query": "Why did you choose debt?"}
    result_2 = graph.invoke(inputs_2)

    assert "answer" in result_2
    assert len(result_2["answer"]) > 50