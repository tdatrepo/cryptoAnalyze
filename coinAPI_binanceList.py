import json

def check_pair(data):
    # if data["quoteAsset"] == "USDT" and data["isMarginTradingAllowed"]:
    return data["symbol"][:-4]

def get_pair():
    # file_path = 'binanceCoin.json'
    file_path = 'futurePair.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    data_list = data['data']
    list_pair = [x for x in map(check_pair, data_list) if x is not None]
    return list_pair

def get_auth_pair():
    # file_path = 'binanceCoin.json'
    file_path = 'futurePair.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    data_list = data['data']
    list_pair = [x for x in map(lambda x: x['symbol'], data_list) if x is not None]
    return list_pair
# print(get_auth_pair())

# a = list(map(check_monkey, data['data']))
# count += sum(a)