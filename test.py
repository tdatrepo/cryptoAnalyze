import json
with open('futureSymbol.json', 'r') as file:
    cryptoTable = json.load(file)

# Giờ đây, 'data' chứa nội dung của file JSON
print(cryptoTable['BTCUSDT'])