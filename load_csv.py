import csv


import requests
import pandas as pd
import time

# Your Alpha Vantage API Key
API_KEY = "266WDXGEPPQWH3FF"  # Change to any stock symbol


# Function to fetch daily stock data (6 months)
def get_daily_stock_data(SYMBOL):
    # Alpha Vantage API URLs
    DAILY_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&outputsize=full&apikey={API_KEY}"

    print("Fetching 6 months daily stock data...")
    response = requests.get(DAILY_URL)
    data = response.json()

    if "Time Series (Daily)" not in data:
        print("Error fetching daily data:", data)
        return None

    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })

    # Keep only the last 6 months
    df = df.sort_index(ascending=False).head(180)
    return df

# Function to fetch intraday stock data (last 5 days, 15-minute intervals)
def get_intraday_stock_data(SYMBOL):
    INTRADAY_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={SYMBOL}&interval=15min&outputsize=full&apikey={API_KEY}"
    print("Fetching 5 days 15-min intraday stock data...")
    response = requests.get(INTRADAY_URL)
    data = response.json()

    if "Time Series (15min)" not in data:
        print("Error fetching intraday data:", data)
        return None

    df = pd.DataFrame.from_dict(data["Time Series (15min)"], orient="index")
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })

    # Keep only the last 5 days of data
    df = df.sort_index(ascending=False).head(5 * 24 * 4)  # 5 days * 24 hours * 4 intervals per hour
    return df



def load_csv(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            empty_row = []
            for i in range(len(row)):
                if i == 0:
                    empty_row.append(row[i])
                else:
                    empty_row.append((row[i]))
            matrix.append(empty_row)
    return matrix

if __name__ == "__main__":
    symbol = "MSFT"
    # Fetch Data
    daily_data = get_daily_stock_data(symbol)
    intraday_data = get_intraday_stock_data(symbol)

    # Save to CSV
    if daily_data is not None:
        daily_data.to_csv("daily_stock_data.csv")
        print("✅ Daily stock data saved to daily_stock_data.csv")

    if intraday_data is not None:
        intraday_data.to_csv("intraday_stock_data.csv")
        print("✅ Intraday stock data saved to intraday_stock_data.csv")

        