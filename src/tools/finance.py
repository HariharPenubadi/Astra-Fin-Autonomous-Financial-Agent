import yfinance as yf
import pandas as pd

def get_company_revenue(company: str, year: int):
    try:
        ticker_map = {
            "apple": "AAPL",
            "tesla": "TSLA",
            "facebook": "META",
            "meta": "META",
            "microsoft": "MSFT"
        }

        ticker = ticker_map.get(company.lower())
        if not ticker:
            return None

        stock = yf.Ticker(ticker)
        income = stock.income_stmt

        if income is None or income.empty:
            return None

        year_to_col = {}
        for col in income.columns:
            if isinstance(col, pd.Timestamp):
                year_to_col[col.year] = col

        if year not in year_to_col:
            return None

        col = year_to_col[year]
        value = income.at["Total Revenue", col]

        if pd.isna(value):
            return None

        return float(value) / 1_000_000_000  # billions

    except Exception as e:
        return None
