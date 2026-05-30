import os
import time
import hashlib
import hmac
import requests

# GitHub Secrets မှ Key များယူခြင်း
API_KEY = os.getenv('MEXC_API_KEY')
SECRET_KEY = os.getenv('MEXC_SECRET_KEY')

# မင်းဝယ်ချင်တဲ့ Coin ၅ မျိုး (Spot Market အတွက်)
# မှတ်ချက် - GOLD အတွက် PAXG ကို သုံးထားပါတယ် (XAUT သည် Futures သာရှိသောကြောင့်ဖြစ်သည်)
SYMBOLS = ["PAXGUSDT", "XLMUSDT", "HYPEUSDT", "SOLUSDT", "BNBUSDT"]
INVEST_PER_COIN = 24.0  # $120 ကို ၅ မျိုးခွဲဝယ်မည်

def get_signature(params):
    query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
    return hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def place_order(symbol):
    endpoint = "https://api.mexc.com/api/v3/order"
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": symbol,
        "side": "BUY",
        "type": "MARKET",
        "quoteOrderQty": INVEST_PER_COIN,
        "timestamp": timestamp,
        "recvWindow": 5000
    }
    params['signature'] = get_signature(params)
    headers = {"X-MEXC-APIKEY": API_KEY}
    return requests.post(endpoint, params=params, headers=headers).json()

def start_bot():
    print("--- Start Buying Coins ---")
    for coin in SYMBOLS:
        try:
            print(f"Buying {coin}...")
            res = place_order(coin)
            print(f"Result for {coin}: {res}")
        except Exception as e:
            print(f"Error buying {coin}: {e}")

if __name__ == "__main__":
    start_bot()
