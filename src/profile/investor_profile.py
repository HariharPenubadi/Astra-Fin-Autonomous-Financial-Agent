import re
from src.memory.semantic import write_semantic


def investor_profile(state):
    query = state["query"].lower()

    # Load existing or default
    profile = state.get("investor_profile", {
        "budget": None,
        "currency": "USD",
        "risk": None,
        "horizon": None,
        "market": "both",
    })

    updated = False

    if any(x in query for x in ["₹", "rupees", "rupee", "rs", "inr"]):
        profile["currency"] = "INR"
    elif any(x in query for x in ["$", "usd", "dollars"]):
        profile["currency"] = "USD"

    matches = re.findall(r"(\d+(?:,\d{3})*(?:\.\d+)?)\s*(k|m)?", query)

    potential_budget = None

    for amount_str, multiplier_str in matches:
        try:
            val = float(amount_str.replace(",", ""))

            if multiplier_str == 'k':
                val *= 1000
            elif multiplier_str == 'm':
                val *= 1000000

            is_year = (1990 < val < 2100)
            if is_year and "budget" not in query and "invest" not in query and "have" not in query:
                continue

            potential_budget = int(val)
        except:
            continue

    if potential_budget and any(x in query for x in ["have", "invest", "budget", "capital", "save", "my money"]):
        profile["budget"] = potential_budget
        write_semantic("budget", str(profile["budget"]))
        if profile.get("currency"):
            write_semantic("currency", profile["currency"])
        updated = True
        print(f"📝 Profile Updated: Budget={profile['budget']} {profile.get('currency')}")

    if any(k in query for k in ["low risk", "low-risk", "safe", "conservative", "secure"]):
        profile["risk"] = "low"
        write_semantic("risk", "low")
        updated = True
    elif any(k in query for k in ["high risk", "aggressive", "crypto", "growth", "high return"]):
        profile["risk"] = "high"
        write_semantic("risk", "high")
        updated = True
    elif any(k in query for k in ["medium", "balanced", "moderate"]):
        profile["risk"] = "medium"
        write_semantic("risk", "medium")
        updated = True

    if any(k in query for k in ["short term", "1 year", "months", "soon"]):
        profile["horizon"] = "short"
        write_semantic("horizon", "short")
        updated = True
    elif any(k in query for k in ["long term", "5 years", "10 years", "retire"]):
        profile["horizon"] = "long"
        write_semantic("horizon", "long")
        updated = True

    state["investor_profile"] = profile
    state["profile_updated"] = updated

    return state