import os
import time
import hashlib
import hmac
import requests

API_KEY = os.getenv('MEXC_API_KEY')
SECRET_KEY = os.getenv('MEXC_SECRET_KEY')

# ဝယ်မည့် Coin ၅ မျိုး (BTC/ETH မပါ)
SYMBOLS = ["PAXGUSDT", "XLMUSDT", "HYPEUSDT", "SOLUSDT", "BNBUSDT"]
INVEST_PER_COIN = 24.0 

def get_signature(params):
    query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
    return hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def get_price(symbol):
    url = f"https://api.mexc.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url).json()
    return float(response['price'])

def place_order(symbol, side):
    endpoint = "https://api.mexc.com/api/v3/order"
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": symbol, "side": side, "type": "MARKET",
        "quoteOrderQty": INVEST_PER_COIN, "timestamp": timestamp, "recvWindow": 5000
    }
    params['signature'] = get_signature(params)
    headers = {"X-MEXC-APIKEY": API_KEY}
    return requests.post(endpoint, params=params, headers=headers).json()

def start_bot():
    print("--- Spot Trading Bot Started ---")
    for coin in SYMBOLS:
        try:
            print(f"Buying {coin}...")
            res = place_order(coin, "BUY")
            print(f"Result: {res}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start_bot()
