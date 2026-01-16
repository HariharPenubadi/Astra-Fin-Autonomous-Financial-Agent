from src.risk.risk_engine import classify_risk
from src.portfolio.allocator import allocate_portfolio
from src.memory.semantic import read_semantic
from src.core.llm import get_llm


def advisor(state):
    llm = get_llm()
    query = state.get("query", "")

    profile = state.get("investor_profile", {})

    if not profile.get("budget"): profile["budget"] = read_semantic("budget")
    if not profile.get("risk"): profile["risk"] = read_semantic("risk")
    if not profile.get("horizon"): profile["horizon"] = read_semantic("horizon")
    if not profile.get("currency"): profile["currency"] = read_semantic("currency") or "USD"

    if not profile.get("budget") or not profile.get("risk"):
        return {
            "answer": "I can certainly help, but I need a bit more info.\n\n**How much are you looking to invest, and do you prefer low, medium, or high risk?**"
        }

    risk_type = classify_risk(profile)
    allocation = allocate_portfolio(risk_type, profile.get("market", "both"))

    specific_advice = ""
    if profile.get("currency") == "INR":
        if risk_type == "aggressive":
            specific_advice = "For Equity, suggest 'Quant Small Cap Fund' or 'Nippon India Small Cap'. For Debt, suggest 'HDFC Short Term Debt Fund'."
        elif risk_type == "conservative":
            specific_advice = "For Equity, suggest 'UTI Nifty 50 Index Fund'. For Debt, suggest 'HDFC Liquid Fund' or 'Bank FDs'."
        else:  # Balanced
            specific_advice = "For Equity, suggest 'Parag Parikh Flexi Cap Fund'. For Debt, suggest 'Corporate Bond Funds'."
    else:
        # USD Fallback
        if risk_type == "aggressive":
            specific_advice = "Suggest 'QQQ' (Tech ETF) and 'Vanguard Growth ETF'."
        else:
            specific_advice = "Suggest 'Vanguard Total Stock Market (VTI)' and 'US Treasury Bills'."

    system_prompt = f"""
    You are ASTRA, a precise financial advisor.

    USER DATA:
    - Budget: {profile['budget']} {profile['currency']}
    - Risk Profile: {risk_type.upper()}
    - Allocation: {allocation}
    - Specific Recommendations To Use: "{specific_advice}"

    TASK:
    Generate a response using EXACTLY this structure:

    1. **Analysis**: "Based on your total budget of {profile['budget']} {profile['currency']}..."
    2. **Allocation Plan**: List the breakdown (Equity, Debt, Gold).
    3. **Specific Recommendations**: You MUST list the specific fund names provided above. (e.g., "For Equity, I recommend...")
    4. **Why?**: Brief explanation.

    USER QUERY: "{query}"
    """

    response = llm.invoke(system_prompt).content

    return {"answer": response}