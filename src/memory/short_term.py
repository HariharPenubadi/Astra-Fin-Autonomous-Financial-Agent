from collections import deque

SHORT_TERM_MEMORY = deque(maxlen=6)

def add_turn(user: str, assistant: str):
    SHORT_TERM_MEMORY.append({
        "user": user,
        "assistant": assistant
    })

def get_context():
    """
    Returns short conversational context for reasoning
    """
    return list(SHORT_TERM_MEMORY)

def clear():
    SHORT_TERM_MEMORY.clear()
