from src.data.data_pipeline import fetch_real_time
import time


def run_live_trading(symbol="AAPL"):
    print(f"Fetching live data for {symbol}...")
    df = fetch_real_time(symbol)
    if not df.empty:
        latest = df.iloc[-1]
        print("Latest Price Info:")
        print(latest)
        # Example logic (dummy)
        close_price = latest["Close"]
        if close_price > latest["Open"]:
            print("Agent decision: BUY")
        else:
            print("Agent decision: SELL")
    else:
        print("No data fetched.")


if __name__ == "__main__":
    while True:
        run_live_trading()
        time.sleep(65)  # Respect Alpha Vantage free tier rate limit
