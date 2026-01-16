def test_hybrid_returns_results():
    from src.retrieval.hybrid import hybrid_retrieve
    result = hybrid_retrieve("Apple revenue")
    assert "vector" in result
