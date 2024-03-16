 #This example uses Python 2.7 and the python-request library.

import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from coinAPI_binanceList import get_pair
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '72e9d4c6-b456-42a6-8bce-e650484c3615',
}

session = Session()
session.headers.update(headers)

binance_list_pair = get_pair()

def check_24h_change(coin):
  price = coin['quote']['USD']['price'] 
  if 'e-'in str(price):
    return
  rate_1h = coin['quote']['USD']['percent_change_1h'] 
  rate_24h = coin['quote']['USD']['percent_change_24h'] 
  rate_7d = coin['quote']['USD']['percent_change_7d'] 

  if rate_1h > 5 and rate_7d < 100 and coin['symbol'] in binance_list_pair:
    entry_price = (2)/100 * price + price
    sl = entry_price * 1.07
    tp =  entry_price * 0.95
    tempVar = {
           's': coin['symbol'],
          'a' : 'sell',
           'p' : round(price, 5),
           'r' : list(map(lambda x: round(x, ndigits=5), [entry_price, tp, sl])),
            '1h': round(rate_1h),
           'n': coin['name'],
           '24h': rate_24h
           }
    print(tempVar)
    return tempVar
  if rate_1h < -5 and rate_7d > -100 and coin['symbol'] in binance_list_pair:
    entry_price = price - (2)/100 * price
    sl = entry_price * 0.93
    tp =  entry_price * 1.05
    tempVar = {
            's': coin['symbol'],
            'a' : 'buy',
            'p' : round(price, 5),
            'r' : list(map(lambda x: round(x, ndigits=5), [entry_price, tp, sl])),
            '1h': round(rate_1h),
            'n': coin['name'],
            '24h': round(rate_24h)}
    print(tempVar)
    return tempVar

def check_90d_change(coin):
  price = coin['quote']['USD']['price'] 
  rate_1h = coin['quote']['USD']['percent_change_1h'] 
  rate_24h = coin['quote']['USD']['percent_change_24h'] 
  rate_7d = coin['quote']['USD']['percent_change_7d'] 
  rate_30d = coin['quote']['USD']['percent_change_30d'] 
  rate_90d = coin['quote']['USD']['percent_change_90d'] 
  # if rate_24h > 20:
  #   print({'symbol': coin['symbol'], 'percent_change_24h': rate_24h, 'remark': 'should_sell'})
  #   return {'symbol': coin['symbol'], 'percent_change_24h': rate_24h, 'remark': 'should_sell'}
  # el
  # if rate_24h > 10 and coin['symbol'] in binance_list_pair:
  if coin['symbol'] in binance_list_pair and rate_90d < 10 and rate_30d < 20:
    print({'symbol': coin['symbol'],
           'price' : round(price, 5),
           'percent_change_30d': rate_30d,
           'percent_change_90d': rate_90d})
    return {'symbol': coin['symbol'], 'percent_change_24h': rate_1h, 'remark': 'should_buy'}

def check_market_cap(coin):
  id = coin['id']
  name = coin['name']
  full_de = coin['quote']['USD']['fully_diluted_market_cap']
  price = coin['quote']['USD']['price'] 
  if 'e-'in str(price):
    return
  symbol = coin['symbol']
  num_market_pairs = coin['num_market_pairs']
  sui_eco = 'sui-ecosystem'
  # if full_de < 50_000_000 and sui_eco in coin['tags']:
  if full_de < 5_000_000 and full_de > 1_000_000 and num_market_pairs in range(30, 60):
    print(id, name, symbol, price)
    
try:
  response = session.get(url, params=parameters)
  json_data = json.loads(response.text) # to json
  print(json_data['status']['timestamp'])
  list_coin = json_data['data'] # to json
  data = json.dumps(json_data)  # to string
  f = open("market.json", "w")
  f.write(data)
  f.close() #[x for x in map(check_24h_change, list_coin) if x is not None] check_market_cap check_24h_change
  result = [x for x in map(check_24h_change, list_coin) if x is not None]
  # print(result)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
  print("FAIL")