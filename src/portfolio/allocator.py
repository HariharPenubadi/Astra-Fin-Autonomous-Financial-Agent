def allocate_portfolio(risk_type, market):
    if risk_type == "conservative":
        return {
            "equity": 30,
            "debt": 50,
            "gold": 20
        }

    if risk_type == "aggressive":
        return {
            "equity": 70,
            "debt": 10,
            "gold": 10,
            "alternative": 10
        }

    return {
        "equity": 50,
        "debt": 30,
        "gold": 20
    }
