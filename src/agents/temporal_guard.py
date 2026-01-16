import re
from datetime import datetime

CURRENT_YEAR = datetime.now().year

def temporal_guard(state):
    query = state["query"]

    years = re.findall(r"\b(20\d{2})\b", query)
    years = [int(y) for y in years]

    for y in years:
        if y >= CURRENT_YEAR:
            return {
                "answer": f"Verified financial revenue data for {y} is not yet available.",
                "memory_locked": True
            }

    return {}
