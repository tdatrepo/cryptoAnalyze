import datetime
import json
from binance.um_futures import UMFutures
from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd
from coinAPI_binanceList import get_auth_pair
import time
from dotenv import load_dotenv
import os

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
binance_list_pair = get_auth_pair()


um_futures_client = UMFutures(key = api_key,
                              secret = api_secret)
# um_futures_client.klines()
# client = Client('SSXkAxuv2Zez5asJ0idZSeuPgyFD9l0ttvc0nbLZDFyQ6HwvWMIDGUlx4WGygufp',
                            #   'YDV8uTGawx9MbnQUPZvCa29qE5uAwhOabpzWaNvvHzhfXUwNyTj4HCreJGrMkbLq')

# um_futures_client = UMFutures()

def check_1h_rate(symbol):
    # klines = um_futures_client.klines(symbol, "1m", **{"limit": 60})
    # klines = client.get_klines(symbol=symbol, interval='15m', limit=1000)
    try:
        # Attempt to retrieve the earliest symbol kline
        klines = um_futures_client.mark_price_klines(symbol, "1m", **{"limit": 120})
    except BinanceAPIException as e:
        # If a BinanceAPIException is raised, catch it and print the error message
        print(f"Error fetching Kline future status: {e.message}")
        time.sleep(5)
        return None
    columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
            'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
    df = pd.DataFrame(klines, columns=columns)
    # df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    # df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    # df['Rate Change (%)'] = round(((df['High'].astype(float) - df['Low'].astype(float)) / df['Low'].astype(float)) * 100)
    last_hour_price = float(df.iloc[0, 1])
    current_price = float(df.iloc[-1, 4])
    temp = current_price - last_hour_price
    if temp != 0:
        result = round(temp/last_hour_price * 100, 2)
    else:
        result = 0
        
    if result > 5 or result < -5:
        print(symbol, ": ", result, "%, price: ", current_price)
        # return result
    # print(symbol, ": ", result, "%")
    time.sleep(0.5)
    return result

def calculate_entry(price):
    entry_price = (2)/100 * price + price
    sl = entry_price * 1.07
    tp =  entry_price * 0.95
    return [str(entry_price), str(tp), str(sl)]
try:
    while True:
        minus = 0
        plus = 0
        total = {
            "5": 0,
            "10": 0,
            "15": 0,
            "100": 0,
            "-5": 0,
            "-10": 0,
            "-15": 0,
            "-100": 0
        }
        intervals = [(0, 5), (5, 10), (10, 15), (15, 100), (-5, 0), (-10, -5), (-15, -10), (-100, -15)]
        print(datetime.datetime.now().time())
        for i in binance_list_pair:
            result = check_1h_rate(i)
            if result < 0:
                minus += 1
            elif result > 0:
                plus += 1
            for i, interval in enumerate(intervals):
                if interval[0] <= result < interval[1]:
                    if result >= 0: total[str(interval[1])] += 1
                    else: total[str(interval[0])] += 1
                    break
        print("minus: ", minus, "plus: ", plus)
        print(total)
except KeyboardInterrupt:
    print("STOP!!!!!!!!!!!!!!!!!!!!!!!!!!!")