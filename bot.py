import os
import ccxt
import pandas as pd
import ta

# API Keys များကို Secrets ထဲမှ ဆွဲယူခြင်း
exchange = ccxt.mexc({
    'apiKey': os.environ.get('MEXC_API_KEY'),
    'secret': os.environ.get('MEXC_SECRET_KEY'),
})

symbol = 'PAXG/USDT' # ရွှေ Coin
timeframe = '5m'

def run_logic():
    try:
        print("Market စစ်ဆေးနေပါသည်...")
        bars = exchange.fetch_ohlcv(symbol, timeframe, limit=300)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['ema200'] = ta.trend.ema_indicator(df['close'], window=200)
        
        last_close = df['close'].iloc[-1]
        last_ema = df['ema200'].iloc[-1]
        
        # Balance စစ်ဆေးခြင်း
        balance = exchange.fetch_balance()
        usdt = balance['total'].get('USDT', 0)
        coin = balance['total'].get('PAXG', 0)
        
        print(f"Price: {last_close} | EMA200: {last_ema}")

        # Buy Strategy
        if last_close < last_ema and usdt > 10:
            print("Buying Gold...")
            exchange.create_market_buy_order(symbol, 10)
            
        # Sell Strategy
        elif last_close > last_ema and coin > 0.0001:
            print("Selling Gold...")
            exchange.create_market_sell_order(symbol, coin)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_logic()
