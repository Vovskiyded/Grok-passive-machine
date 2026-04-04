import os
import telebot

TOKEN = "ВСТАВЬ_СВОЙ_ТОКЕН_БОТА"
WALLET = "ВСТАВЬ_СВОЙ_USDT_АДРЕС"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Каталог товаров:\n1. Тестовый товар — 10 USDT\nНапиши номер товара")

@bot.message_handler(func=lambda m: True)
def handle(m):
    if m.text.isdigit():
        bot.reply_to(m, f"Оплата 10 USDT на {WALLET}\nПосле оплаты напиши «ОПЛАТИЛ»")
    elif "ОПЛАТИЛ" in m.text.upper():
        bot.reply_to(m, "✅ Товар отправлен! Спасибо за покупку.")

bot.infinity_polling()
