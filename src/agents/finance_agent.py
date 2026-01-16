import json
import re
from src.tools.finance import get_company_revenue
from src.core.llm import get_llm
from src.retrieval.web import web_retrieve


def finance_agent(state):
    query = state["query"]
    llm = get_llm()


    extraction_prompt = f"""
    Extract entity and year from: "{query}"
    Return STRICT JSON: {{"company": "Apple", "year": 2023}}
    No extra text.
    """

    try:
        raw = llm.invoke(extraction_prompt).content
        raw = raw.replace("```json", "").replace("```", "").strip()
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end != -1:
            json_str = raw[start:end]
            data = json.loads(json_str)
        else:
            data = {"company": None}
    except:
        data = {"company": None}

    if data.get("company") and data.get("year"):
        print(f"🛠️ Calling Tool: Revenue for {data['company']} in {data['year']}")
        revenue = get_company_revenue(data["company"], int(data["year"]))
        if revenue:
            return {
                "answer": f"💰 **Financial Fact**: {data['company'].title()}'s revenue in {data['year']} was approximately **${revenue:.1f} billion** (USD).",
                "memory_locked": True
            }

    print(f"🔍 Tool unavailble. Searching web for: {query}")
    web_results = web_retrieve(query)

    if not web_results:
        return {"answer": "I'm sorry, I couldn't verify that financial data right now."}

    context = "\n".join([r['content'] for r in web_results[:3]])

    summary = llm.invoke(
        f"User asked: '{query}'\n\nBased on these search results, provide a direct answer (with numbers if available):\n{context}"
    ).content

    return {
        "answer": summary,
        "memory_locked": True
    }