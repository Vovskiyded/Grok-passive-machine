import ccxt
import time

# === ВСТАВЬ СВОИ КЛЮЧИ ===
binance = ccxt.binance({'apiKey': 'ВАШ_API_KEY', 'secret': 'ВАШ_SECRET'})
bybit = ccxt.bybit({'apiKey': 'ВАШ_API_KEY', 'secret': 'ВАШ_SECRET'})

MIN_PROFIT = 0.004  # 0.4%

while True:
    try:
        p1 = binance.fetch_ticker('BTC/USDT')['last']
        p2 = bybit.fetch_ticker('BTC/USDT')['last']
        diff = (p2 - p1) / p1 * 100

        if diff > MIN_PROFIT * 100:
            print(f"🚀 Возможность! Купить Binance {p1:.2f} → Продать Bybit {p2:.2f} (+{diff:.2f}%)")
        time.sleep(2)
    except:
        time.sleep(5)
