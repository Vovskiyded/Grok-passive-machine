# ================================================
# ИНСТРУКЦИЯ ДЛЯ ЭТОГО ФАЙЛА (Arbitrage Bot)
# ================================================
# 1. Этот бот ищет разницу цен на биржах и показывает прибыльные сделки.
# 2. Замени YOUR_API_KEY и YOUR_API_SECRET на реальные ключи от Binance/Bybit.
# 3. Запусти бота — он будет работать 24/7.
# 4. После покупки клиент получит этот файл и сможет сразу использовать.
# ================================================

import ccxt
import time

# ←←← ЗАМЕНИ НА СВОИ КЛЮЧИ ←←←
binance = ccxt.binance({
    'apiKey': 'YOUR_BINANCE_API_KEY',
    'secret': 'YOUR_BINANCE_API_SECRET'
})

bybit = ccxt.bybit({
    'apiKey': 'YOUR_BYBIT_API_KEY',
    'secret': 'YOUR_BYBIT_API_SECRET'
})

print("🚀 Арбитраж-бот запущен. Ищем возможности...")

while True:
    try:
        p1 = binance.fetch_ticker('BTC/USDT')['last']
        p2 = bybit.fetch_ticker('BTC/USDT')['last']
        diff = (p2 - p1) / p1 * 100
        if diff > 0.4:
            print(f"✅ ВОЗМОЖНОСТЬ! Купить на Binance {p1:.2f} → Продать на Bybit {p2:.2f} (+{diff:.2f}%)")
        time.sleep(3)
    except:
        time.sleep(5)
