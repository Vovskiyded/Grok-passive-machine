import os
import telebot

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CRYPTO_WALLET = os.getenv('CRYPTO_WALLET')
ADMIN_ID = int(os.getenv('ADMIN_CHAT_ID'))

bot = telebot.TeleBot(TELEGRAM_TOKEN)

PRODUCTS = {
    "1": {"name": "Готовый бот для авто-продаж", "price": 25},
    "2": {"name": "100 промптов Grok-OMEGA", "price": 12},
    "3": {"name": "Арбитраж-бот", "price": 37}
}

@bot.message_handler(commands=['start', 'catalog'])
def catalog(message):
    text = "🛒 Grok-OMEGA Store — деньги без участия\n\n"
    for k, p in PRODUCTS.items():
        text += f"{k}. {p['name']} — {p['price']} USDT\n"
    text += "\nНапиши номер товара"
    bot.reply_to(message, text)

@bot.message_handler(func=lambda m: True)
def buy(message):
    choice = message.text.strip()
    if choice in PRODUCTS:
        p = PRODUCTS[choice]
        bot.reply_to(message, f"✅ Вы выбрали: {p['name']}\n\nОплата: {p['price']} USDT (TRC20)\nПереведи на:\n{CRYPTO_WALLET}\n\nПосле оплаты напиши «ОПЛАТИЛ {choice}»")
    else:
        bot.reply_to(message, "Напиши /catalog")

print("🚀 Упрощённый бот запущен и готов продавать")
bot.infinity_polling()
