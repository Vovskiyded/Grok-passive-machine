import os
import telebot
import requests
import time

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CRYPTO_WALLET = os.getenv('CRYPTO_WALLET')
ADMIN_ID = int(os.getenv('ADMIN_CHAT_ID'))

bot = telebot.TeleBot(TELEGRAM_TOKEN)

PRODUCTS = {
    "1": {"name": "Готовый бот для авто-продаж", "price": 25, "file": "sales_bot.py"},
    "2": {"name": "100 промптов Grok-OMEGA", "price": 12, "file": "prompts.txt"},
    "3": {"name": "Арбитраж-бот", "price": 37, "file": "arbitrage_bot.py"}
}

# Проверка транзакции TRC20
def check_trx(txid, expected_amount_usdt):
    try:
        url = f"https://apilist.tronscanapi.com/api/transaction?hash={txid}"
        resp = requests.get(url, timeout=10).json()
        if not resp.get('data'):
            return False, "Транзакция не найдена"
        
        tx = resp['data'][0]
        if tx['ownerAddress'] == CRYPTO_WALLET.lower() and tx['toAddress'] == CRYPTO_WALLET.lower():
            amount = tx.get('amount', 0) / 1_000_000  # USDT = 6 decimals
            if amount >= expected_amount_usdt - 0.5:  # небольшая погрешность
                return True, f"✅ Оплата {amount} USDT подтверждена"
        return False, "Сумма или адрес не совпадает"
    except:
        return False, "Ошибка проверки TXID"

@bot.message_handler(commands=['start', 'catalog'])
def catalog(message):
    text = "🛒 Grok-OMEGA Store — деньги без участия\n\n"
    for k, p in PRODUCTS.items():
        text += f"{k}. {p['name']} — {p['price']} USDT\n"
    text += "\nНапиши номер товара"
    bot.reply_to(message, text)

@bot.message_handler(func=lambda m: True)
def handle(message):
    text = message.text.strip().upper()
    
    if "ОПЛАТИЛ" in text:
        try:
            num = text.split()[1]
            if num not in PRODUCTS:
                bot.reply_to(message, "Неверный номер")
                return
            p = PRODUCTS[num]
            bot.reply_to(message, f"✅ Вы выбрали: {p['name']}\n\nОтправь TXID транзакции (из Trust Wallet или TronScan)")
            bot.register_next_step_handler(message, lambda m: process_payment(m, num))
        except:
            bot.reply_to(message, "Напиши «ОПЛАТИЛ X», где X — номер товара")
    else:
        bot.reply_to(message, "Напиши /catalog")

def process_payment(message, num):
    txid = message.text.strip()
    p = PRODUCTS[num]
    
    bot.reply_to(message, "🔍 Проверяю оплату...")
    success, msg = check_trx(txid, p['price'])
    
    if success:
        bot.reply_to(message, msg)
        # Отправляем файл
        try:
            with open(p['file'], "rb") as f:
                bot.send_document(message.chat.id, f, caption=f"🎉 Вот твой товар: {p['name']}")
            bot.send_message(ADMIN_ID, f"🎉 Продажа! Клиент купил {p['name']} (TXID: {txid})")
        except:
            bot.reply_to(message, "Файл готов, но произошла ошибка отправки. Напиши @Volodya")
    else:
        bot.reply_to(message, f"❌ {msg}\nПроверь TXID и попробуй ещё раз.")

print("🚀 Бот с авто-проверкой оплаты запущен")
bot.infinity_polling()
