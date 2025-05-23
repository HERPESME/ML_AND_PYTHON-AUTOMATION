from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time


def fetch_real_time(symbol, api_key, interval="1min", max_retries=3):
    ts = TimeSeries(key=api_key, output_format="pandas")
    for attempt in range(max_retries):
        try:
            data, _ = ts.get_intraday(
                symbol=symbol, interval=interval, outputsize="compact"
            )
            data = (
                data.rename(
                    columns={
                        "1. open": "Open",
                        "2. high": "High",
                        "3. low": "Low",
                        "4. close": "Close",
                        "5. volume": "Volume",
                    }
                )
                .reset_index()
                .rename(columns={"date": "Date"})
            )
            return data
        except Exception as e:
            print(f"Error fetching data (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(12)
    raise RuntimeError("Failed to fetch real-time data after multiple attempts")


def stream_realtime_data(symbol, api_key, duration_minutes=5, interval_seconds=60):
    end_time = time.time() + duration_minutes * 60
    print(f"Starting real-time stream for {symbol}...")
    while time.time() < end_time:
        df = fetch_real_time(symbol, api_key)
        latest = df.sort_values(by="Date", ascending=False).iloc[0]
        print(f"[{latest['Date']}] Price: {latest['Close']}")
        # You can pass `latest` to the RL agent here
        time.sleep(interval_seconds)


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    SYMBOL = "AAPL"
    stream_realtime_data(SYMBOL, API_KEY, duration_minutes=5, interval_seconds=60)
