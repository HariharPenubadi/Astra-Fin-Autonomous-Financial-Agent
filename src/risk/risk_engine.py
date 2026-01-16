def classify_risk(profile):
    risk = profile.get("risk")
    horizon = profile.get("horizon")

    if risk == "low":
        return "conservative"

    if risk == "high":
        return "aggressive"

    return "balanced"