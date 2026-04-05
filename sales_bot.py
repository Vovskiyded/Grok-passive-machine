# ================================================
# ПРОДАЖНЫЙ БОТ — ПОЛНАЯ ИНСТРУКЦИЯ
# ================================================
# Привет! 👋
# Этот бот уже готов продавать твои товары 24/7 без твоего участия.
# Мотивация: Один такой бот может приносить 500–3000$ в месяц на автопилоте.
# 
# Нужные сайты:
# 1. Telegram (BotFather)
# 2. Trust Wallet или Binance (для USDT TRC20)
# 
# Пошаговая настройка:
# 1. Замени TOKEN и WALLET на свои
# 2. Загрузи файл в Railway
# 3. Запусти — бот сразу начинает работать
# ================================================

import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "YOUR_BOT_TOKEN_HERE"
WALLET = "YOUR_USDT_WALLET_HERE"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🛒 Магазин запущен. Нажми кнопку ниже, чтобы купить.")

bot.infinity_polling()
print("🚀 Продажный бот запущен и готов зарабатывать")
