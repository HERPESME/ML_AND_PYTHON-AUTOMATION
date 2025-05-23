import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"


def fetch_data(symbol="AAPL", interval="daily", outputsize="full"):
    if interval == "daily":
        function = "TIME_SERIES_DAILY_ADJUSTED"
        params = {
            "function": function,
            "symbol": symbol,
            "outputsize": outputsize,
            "apikey": ALPHA_VANTAGE_API_KEY,
        }
    else:
        raise ValueError("Currently only 'daily' interval is supported.")

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "Time Series (Daily)" not in data:
        raise ValueError(f"API Error: {data.get('Note', data)}")

    df = pd.DataFrame.from_dict(
        data["Time Series (Daily)"], orient="index", dtype=float
    )
    df.columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume",
        "Dividend",
        "Split Coef",
    ][: len(df.columns)]
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    os.makedirs("data/historical", exist_ok=True)
    save_path = os.path.join("data", "historical", f"{symbol}.csv")
    df.to_csv(save_path)
    print(f"Data for {symbol} saved to {save_path}")
    return df


if __name__ == "__main__":
    fetch_data("AAPL")
