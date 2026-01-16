import re

def normalize_numbers(answer: str) -> str:
    match = re.search(r"\$([\d,.]+)", answer)
    if not match:
        return answer

    value = float(match.group(1).replace(",", ""))

    if value > 10_000 and value < 1_000_000:
        value = value / 1000
        return f"${value:.1f} billion (USD)"

    if value >= 1_000_000:
        value = value / 1_000_000
        return f"${value:.1f} billion (USD)"

    return answer
