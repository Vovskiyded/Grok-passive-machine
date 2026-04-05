# ================================================
# ПРОДВИНУТАЯ ВОРОНКА ПРОДАЖ — ПОЛНАЯ ИНСТРУКЦИЯ
# ================================================
# Привет! 👋
# Это 5-шаговая воронка, которая сама продаёт твои товары.
# Мотивация: Одна такая воронка может приносить 2000–7000$ в месяц.
# 
# Нужные сайты:
# 1. Telegram (BotFather)
# 2. Trust Wallet
# 
# Пошаговая последовательность:
# 1. Замени TOKEN и WALLET
# 2. Запусти
# 3. Поделись ссылкой на бота
# 4. Получай продажи автоматически
# ================================================

import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "YOUR_BOT_TOKEN_HERE"
WALLET = "YOUR_USDT_WALLET_HERE"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Добро пожаловать в воронку! Нажми кнопку ниже, чтобы купить.")
