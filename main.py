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
          "teaser": "Тизер: Этот бот автоматически показывает каталог, принимает оплату и выдаёт товары 24/7. Полный код с авто-доставкой — после оплаты."},
    "2": {"ru": "100 промптов Grok-OMEGA", "en": "100 Grok-OMEGA prompts", "price": 12, "file": "prompts.txt",
          "teaser": "Тизер: 100 самых мощных промптов для бизнеса и заработка. Вот первые 3 примера (полный список 100 — после оплаты)."},
    "3": {"ru": "Арбитраж-бот", "en": "Arbitrage bot", "price": 37, "file": "arbitrage_bot.py",
          "teaser": "Тизер: Автоматически ищет разницу цен на биржах и показывает прибыльные возможности. Полный код — после оплаты."},
    "4": {"ru": "TikTok Автопостинг бот", "en": "TikTok Auto-Poster Bot", "price": 59, "file": "tiktok_bot.py",
          "teaser": "Тизер: Генерирует видео + текст и публикует в TikTok каждые 4 часа без твоего участия. Полный код — после оплаты."},
    "5": {"ru": "Продвинутая воронка продаж", "en": "Advanced Sales Funnel", "price": 49, "file": "funnel_bot.py",
          "teaser": "Тизер: 5-шаговая воронка, которая автоматически ведёт клиента от приветствия до оплаты. Полная настройка — после оплаты."},
    "6": {"ru": "Faceless Content Pack", "en": "Faceless Content Pack", "price": 39, "file": "faceless_pack.txt",
          "teaser": "Тизер: 50 готовых идей контента без лица + шаблоны. Полный пак с 200+ материалами — после оплаты."},
    "7": {"ru": "Lead Generation Bot", "en": "Lead Generation Bot", "price": 35, "file": "lead_bot.py",
          "teaser": "Тизер: Автоматически собирает контакты из чатов и каналов. Полный код с парсингом — после оплаты."},
    "8": {"ru": "Passive Income Blueprint", "en": "Passive Income Blueprint", "price": 27, "file": "blueprint.txt",
          "teaser": "Тизер: Пошаговый план запуска пассивного дохода от 1000$ в месяц. Полный blueprint — после оплаты."}
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"))
    markup.add(InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"))
    bot.reply_to(message, "Привет! 👋\n\nВыбери язык / Choose language:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    lang = call.data.split('_')[1]
    current_lang[call.from_user.id] = lang
    bot.answer_callback_query(call.id)
    show_catalog(call.message)

def show_catalog(message):
    lang = current_lang.get(message.chat.id, 'ru')
    text = "🛒 Grok-OMEGA Store — passive income\n\n"
    markup = InlineKeyboardMarkup(row_width=1)
    for k, p in PRODUCTS.items():
        text += str(k) + ". " + p[lang] + " — $" + str(p['price']) + "\n"
        markup.add(InlineKeyboardButton(str(k) + ". " + p[lang], callback_data="buy_" + str(k)))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def buy_callback(call):
    num = call.data.split('_')[1]
    p = PRODUCTS[num]
    lang = current_lang.get(call.from_user.id, 'ru')
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, p['teaser'])
    bot.send_message(call.message.chat.id,
        "✅ Вы выбрали: " + p[lang] + "\n\nОплата: $" + str(p['price']) + " USDT (TRC20)\nПереведи на:\n" + CRYPTO_WALLET + "\n\nПосле оплаты
