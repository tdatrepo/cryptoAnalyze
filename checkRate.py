import json
from binance.um_futures import UMFutures
# from binance.client import Client
import pandas as pd
# import numpy as np
# from coinAPI_binanceList import get_auth_pair
from teleBot import send_telegram_message
import time
import json
import datetime

# Giờ đây, 'data' chứa nội dung của file JSON
# binance_list_pair = get_auth_pair()

# um_futures_client = UMFutures(key='SSXkAxuv2Zez5asJ0idZSeuPgyFD9l0ttvc0nbLZDFyQ6HwvWMIDGUlx4WGygufp',
#                               secret='YDV8uTGawx9MbnQUPZvCa29qE5uAwhOabpzWaNvvHzhfXUwNyTj4HCreJGrMkbLq')
um_futures_client = UMFutures()
# client = Client('SSXkAxuv2Zez5asJ0idZSeuPgyFD9l0ttvc0nbLZDFyQ6HwvWMIDGUlx4WGygufp',
#                               'YDV8uTGawx9MbnQUPZvCa29qE5uAwhOabpzWaNvvHzhfXUwNyTj4HCreJGrMkbLq')
# um_futures_client = UMFutures()
# symbol = 'BTCUSDT'

def check_rate(kwargs):
    symbol = kwargs.get('symbol', '')
    symbolValue = kwargs.get('symbolValue', {})
    interval = kwargs.get('interval', 0)
    amount = kwargs.get('amount', 0)
    check_rate_var = kwargs['futureRate']
    
    klines = um_futures_client.klines(symbol, interval, **{"limit": amount})
    # klines = client.get_klines(symbol=symbol, interval='1h', limit=24)
    # klines = client.get_klines(symbol=symbol, interval='15m', limit=1000)
    columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
            'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
    df = pd.DataFrame(klines, columns=columns)
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    # df['Rate Change (%)'] = round(((df['High'].astype(float) - df['Low'].astype(float)) / df['Low'].astype(float)) * 100)
    if check_rate_var['long']:
        last_hour_price = float(df['High'].max())
    elif check_rate_var['short']:
        last_hour_price = float(df['Low'].min())
    else: last_hour_price = float(df.iloc[0, 1])

    current_price = float(df.iloc[-1, 4])
    temp = current_price - last_hour_price
    if temp != 0:
        result = round(temp/last_hour_price * 100, 2)
    else:
        result = 0

    check_rate_var['value'] = result
    check_rate_var['price'] = current_price
    check_rate_var['pricePre'] = last_hour_price
    check_rate_result(check_rate_var)
    # if result > 5:
    #     msg = f'{symbol} is growth {result}%'
    #     print(symbol, ": ", result, "%")
    #     return True
    # else:
    #     # send_telegram_message('#####Not enought to short#####')
    #     print('#####Not enought to short#####',symbol, ": ", result, "%")
    #     return False
    # time.sleep(60)
    # return None
    # print(symbol, ": ", result, "%")\

def check_rate_result(kwagrs):
    symbol = kwagrs.get('symbol')
    short = kwagrs.get('short', False)
    long = kwagrs.get('long', False)
    value = kwagrs.get('value', 'Default value') # current % change
    price = kwagrs.get('price', 'Default price' )
    remark = kwagrs.get('remark', 'no remark')
    pricePre = kwagrs.get('pricePre')
    if short:   # to make a short, the value should greater than shortValue that we expected.
        shortValue = kwagrs.get('shortValue') # '> 0' % change that go up
        if value > shortValue:
            msg = f'SHORT : {symbol} is growth {value}%, price: {price}, {remark}'
            print(msg)
            send_telegram_message(msg)
        else:
            print(f'#####Not enought to short##### {symbol}: {value}% {price} , lowest: {pricePre}, {remark}')
    if long:
        longValue = kwagrs.get('longValue') # '< 0' % change that go down
        if value < longValue:
            msg =  f'LONG : {symbol} is down {value}%, price: {price}, {remark}'
            print(msg)
            send_telegram_message(msg)
        else:
            print(f'#####Not enought to long##### {symbol}: {value}% {price} , highest: {pricePre}, {remark}')
        # pass

    # type_check = kwagrs['type']
    # value = kwagrs['result']
    

if __name__ == '__main__':

    listToken = ['BTCUSDT', 'DOGSUSDT', 'CATIUSDT', 'HMSTRUSDT']
    keyStop = True
    while keyStop:
        try:
            with open('futureSymbol.json', 'r') as file:
                cryptoTable = json.load(file)
            for i in cryptoTable:
                check_rate(cryptoTable[i])
                now = datetime.datetime.now()
                print(now)
                # print(i)
                time.sleep(70)
        except KeyboardInterrupt:
            keyStop = False
            print('Stop by key')
        except:
            print("ERROR, stop for 2 minute")
            time.sleep(120)