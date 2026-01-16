def classify_risk(profile):
    risk = profile["risk"]
    horizon = profile["horizon"]

    if risk == "low":
        return "conservative"
    if risk == "high" and horizon == "long":
        return "aggressive"
    return "balanced"
