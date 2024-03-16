import requests
import json
import pandas as pd
from datetime import datetime

# Binance API Base URL
BASE_URL = 'https://api.binance.com/api/v3'

# Symbol (e.g., BTCUSDT for Bitcoin to USDT)
SYMBOL = 'BTCUSDT'

# Time interval (e.g., 1h for 1-hour candles)
INTERVAL = '1h'

def get_candlestick_data(symbol, interval):
    url = f"{BASE_URL}/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': 100,  # Number of candles to retrieve (adjust as needed)
    }

    response = requests.get(url, params=params)
    data = response.json()

    if isinstance(data, list) and len(data) > 0:
        # Extract relevant data and create a DataFrame
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df

    return None

if __name__ == '__main__':
    candlestick_data = get_candlestick_data(SYMBOL, INTERVAL)

    if candlestick_data is not None:
        print(candlestick_data)
    else:
        print(f"Failed to fetch candlestick data for {SYMBOL} - {INTERVAL}")
