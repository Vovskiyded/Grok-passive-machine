import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CRYPTO_WALLET = os.getenv('CRYPTO_WALLET')
ADMIN_ID = int(os.getenv('ADMIN_CHAT_ID'))

bot = telebot.TeleBot(TELEGRAM_TOKEN)

current_lang = {}

PRODUCTS = {
    "1": {"ru": "Готовый бот для авто-продаж", "en": "Ready sales bot", "price": 25, "file": "sales_bot.py",
          "teaser": "🔹 Тизер: Этот бот автоматически показывает каталог, принимает оплату и выдаёт товары 24/7. Полный код с авто-доставкой — после оплаты."},
    "2": {"ru": "100 промптов Grok-OMEGA", "en": "100 Grok-OMEGA prompts", "price": 12, "file": "prompts.txt",
          "teaser": "🔹 Тизер: 100 самых мощных промптов для бизнеса и заработка. Вот первые 3 примера (полный список 100 — после оплаты)."},
    "3": {"ru": "Арбитраж-бот", "en": "Arbitrage bot", "price": 37, "file": "arbitrage_bot.py",
          "teaser": "🔹 Тизер: Автоматически ищет разницу цен на биржах и показывает прибыльные возможности. Полный код — после оплаты."},
    "4": {"ru": "TikTok Автопостинг бот", "en": "TikTok Auto-Poster Bot", "price": 59, "file": "tiktok_bot.py",
          "teaser": "🔹 Тизер: Генерирует видео + текст и публикует в TikTok каждые 4 часа без твоего участия. Полный код — после оплаты."},
    "5": {"ru": "Продвинутая воронка продаж", "en": "Advanced Sales Funnel", "price": 49, "file": "funnel_bot.py",
          "teaser": "🔹 Тизер: 5-шаговая воронка, которая автоматически ведёт клиента от приветствия до оплаты. Полная настройка — после оплаты."},
    "6": {"ru": "Faceless Content Pack", "en": "Faceless Content Pack", "price": 39, "file": "faceless_pack.txt",
          "teaser": "🔹 Тизер: 50 готовых идей контента без лица + шаблоны. Полный пак с 200+ материалами — после оплаты."},
    "7": {"
