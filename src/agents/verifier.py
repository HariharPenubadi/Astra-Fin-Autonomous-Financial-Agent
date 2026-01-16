def verifier(state):
    if state.get("memory_locked"):
        return {}

    context = state.get("context", "")
    if not context.strip():
        return {
            "answer": "I don't have enough reliable information to answer that accurately.",
            "memory_locked": True
        }

    return {}
