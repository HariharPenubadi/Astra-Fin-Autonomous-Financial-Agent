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


    market_context = ""
    if profile.get("currency") == "INR":
        market_context = """
        INDIAN MARKET EXAMPLES (Use these if user asks for specific names):
        - SAFE / DEBT: 
          * Liquid Funds: SBI Liquid Fund, HDFC Liquid Fund.
          * Fixed Deposits (FDs): HDFC Bank FD, ICICI Bank FD.
        - LOW RISK EQUITY (Large Cap): 
          * Passive: UTI Nifty 50 Index Fund, Navi Nifty 50.
          * Active: Mirae Asset Large Cap.
        - HIGH RISK EQUITY (Mid/Small Cap):
          * Flexi Cap: Parag Parikh Flexi Cap Fund.
          * Small Cap: Quant Small Cap Fund, Nippon India Small Cap.
        - GOLD: Sovereign Gold Bonds (SGB) (Best), Nippon India Gold BEES (ETF).
        """
    else:
        market_context = """
        US/GLOBAL MARKET EXAMPLES:
        - SAFE: US Treasury Bills (BIL), Vanguard Total Bond Market (BND).
        - EQUITY (Growth): Vanguard S&P 500 (VOO), Invesco QQQ (Tech/High Risk).
        - DIVIDEND: Schwab US Dividend Equity (SCHD).
        """

    system_prompt = f"""
    You are ASTRA, an expert financial advisor.

    USER PROFILE:
    - Budget: {profile['budget']} {profile['currency']}
    - Risk Level: {risk_type.upper()}
    - Calculated Allocation: {allocation}

    {market_context}

    USER QUERY: "{query}"

    GUIDELINES:
    1. **Direct Answer:** If user asks "Where to invest?", start with the Allocation Plan (Bullet points with ₹ amounts).
    2. **Be Specific:** If the user asks for "Exact names" or "Which fund?", YOU MUST pick examples from the list above. Do not be vague.
    3. **Explain Why:** Briefly explain why a specific choice fits their {risk_type} profile (e.g., "Quant Small Cap fits your high-risk preference because...").
    4. **Context Update:** If the user JUST changed their risk (e.g., "What if I want high risk?"), acknowledge the switch: "Switching to a High Risk strategy..."
    5. **Disclaimer:** Keep it brief at the bottom.
    """

    response = llm.invoke(system_prompt).content

    return {"answer": response}