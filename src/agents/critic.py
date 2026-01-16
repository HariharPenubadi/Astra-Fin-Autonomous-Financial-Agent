from src.memory.episodic import store_episode

def critic(state):
    query = state["query"]
    answer = state.get("answer", "")

    if answer:
        store_episode(query, answer)

    return {"review": "Answer delivered"}

