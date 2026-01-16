from src.core.llm import get_llm
from src.memory.short_term import get_context

VALID_INTENTS = {
    "greeting",
    "identity",
    "investment_setup",
    "investment_advice",
    "finance_fact",
    "memory_question",
    "general_query",
}


def planner(state):
    llm = get_llm()
    query = state["query"]

    history = get_context()
    history_str = "\n".join([f"User: {h['user']}\nAssistant: {h['assistant']}" for h in history])

    prompt = f"""
You are the Router for a financial AI. Analyze the CURRENT QUERY to determine the user's intent.

DEFINITIONS:
1. **investment_setup**: User provides PERSONAL financial info (e.g., "I have 2000", "My risk is high", "I want to invest $500", "I have 20k savings").
2. **investment_advice**: User asks for PERSONAL recommendations (e.g., "Where should I invest?", "What is a good portfolio for me?", "How to allocate?").
3. **finance_fact**: User asks about EXTERNAL Market Data (e.g., "Apple revenue", "Price of Gold", "GDP of India", "News on Tesla").
4. **greeting**: "Hello", "Hi".
5. **identity**: "Who are you?".
6. **memory_question**: "What did we discuss?".
7. **general_query**: Everything else (e.g. "Why?", "Explain more").

HISTORY:
{history_str}

CURRENT QUERY:
{query}

EXAMPLES:
- "I have 2000 rupees" -> investment_setup
- "Where should I invest?" -> investment_advice
- "Apple revenue" -> finance_fact
- "What is the price of Bitcoin?" -> finance_fact

Classify the intent into EXACTLY ONE label from the list above. Return ONLY the label.
"""

    raw = llm.invoke(prompt).content.lower().strip()

    intent = raw.split()[0].replace(".", "").replace('"', '')

    if intent not in VALID_INTENTS:
        intent = "general_query"

    print(f"🧠 PLANNER: {intent}")
    return {"intent": intent}