import datetime
import json
from binance.um_futures import UMFutures
from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd
from coinAPI_binanceList import get_auth_pair
import time
binance_list_pair = get_auth_pair()


um_futures_client = UMFutures(key='SSXkAxuv2Zez5asJ0idZSeuPgyFD9l0ttvc0nbLZDFyQ6HwvWMIDGUlx4WGygufp',
                              secret='YDV8uTGawx9MbnQUPZvCa29qE5uAwhOabpzWaNvvHzhfXUwNyTj4HCreJGrMkbLq')
# um_futures_client.klines()
# client = Client('SSXkAxuv2Zez5asJ0idZSeuPgyFD9l0ttvc0nbLZDFyQ6HwvWMIDGUlx4WGygufp',
                            #   'YDV8uTGawx9MbnQUPZvCa29qE5uAwhOabpzWaNvvHzhfXUwNyTj4HCreJGrMkbLq')

# um_futures_client = UMFutures()

def check_1h_rate(symbol):
    # klines = um_futures_client.klines(symbol, "1m", **{"limit": 60})
    # klines = client.futures_klines(symbol=symbol, interval='1m', limit=60)
    # klines = client.futures_klines(symbol=symbol, interval='1m', limit=60)
    # klines = client.get_klines(symbol=symbol, interval='15m', limit=1000)
    try:
        # Attempt to retrieve the earliest symbol kline
        klines = um_futures_client.mark_price_klines(symbol, "1m", **{"limit": 30})
        # klines = um_futures_client.klines(symbol, "1m", **{"limit": 60})
        # klines = client.futures_klines(symbol=symbol, interval='1m', limit=60)
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
        return {
            "symbol": symbol,
            "result": result
        }
    # print(symbol, ": ", result, "%")
    time.sleep(0.5)
    return None

def calculate_entry(price):
    entry_price = (2)/100 * price + price
    sl = entry_price * 1.07
    tp =  entry_price * 0.95
    return [str(entry_price), str(tp), str(sl)]
try:
    while True:
        print(datetime.datetime.now().time())
        for i in binance_list_pair:
            check_1h_rate(i)
        # time.sleep(60)
except KeyboardInterrupt:
    print("STOP!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # # Close the WebSocket connection on KeyboardInterrupt
    # bsm.stop_socket(conn_key)
    # bsm.close()

#     break
# map(check_1h_rate, binance_list_pair)
# data = {
#     'time' : um_futures_client.time(),
#     'data' : [] # store trading pair,
# }

# def check_pair(pair):
#     if "USDT" in pair['symbol']:
#         return pair
#     return None
# Get account information
# pair_list = [x for x in map(check_pair, um_futures_client.ticker_price()) if x is not None]
# print(um_futures_client.("BTCUSDT"))
# data['data'] = pair_list
# data = json.dumps(data)  # to string
# f = open("futurePair.json", "w")
# f.write(data)
# f.close()
# Replace 'BTCUSDT' with the trading pair you are interested in
# symbol = 'BTCUSDT'

# # Get the 1-hour klines (candlestick) data
# klines = client.get_klines(symbol=symbol, interval='1h', limit=2)

# # Extract the price change percentage for the last 1 hour
# price_change_1h = float(klines[0][7])  # Close price of the last 1-hour candle
# columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
#            'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
# df = pd.DataFrame(klines, columns=columns)

# # Convert timestamp columns to datetime format
# df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
# df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
# df['Rate Change (%)'] = ((df['High'].astype(float) - df['Low'].astype(float)) / df['Low'].astype(float)) * 100

# # Display the updated DataFrame
# print(df['Rate Change (%)'])
# print(f"Price Change in the last 1 hour for {symbol}: {price_change_1h}%")