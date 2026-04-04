import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CRYPTO_WALLET = os.getenv('CRYPTO_WALLET')
ADMIN_ID = int(os.getenv('ADMIN_CHAT_ID'))

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Языки
LANGUAGES = {
    'ru': '🇷🇺 Русский',
    'en': '🇬🇧 English'
}

current_lang = {}  # user_id -> 'ru' или 'en'

PRODUCTS = {
    "1": {"ru": "Готовый бот для авто-продаж", "en": "Ready sales bot", "price": 25, "file": "sales_bot.py"},
    "2": {"ru": "100 промптов Grok-OMEGA", "en": "100 Grok-OMEGA prompts", "price": 12, "file": "prompts.txt"},
    "3": {"ru": "Арбитраж-бот", "en": "Arbitrage bot", "price": 37, "file": "arbitrage_bot.py"}
}

def get_text(user_id, key):
    lang = current_lang.get(user_id, 'ru')
    texts = {
        'catalog': {'ru': '🛒 Grok-OMEGA Store — деньги без участия\n\n', 'en': '🛒 Grok-OMEGA Store — money without effort\n\n'},
        'choose': {'ru': 'Выбери товар:', 'en': 'Choose product:'},
        'paid': {'ru': '✅ Оплата подтверждена! Отправляю товар...', 'en': '✅ Payment confirmed! Sending your product...'}
    }
    return texts.get(key, {}).get(lang, '')

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"))
    markup.add(InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"))
    bot.reply_to(message, "Выбери язык / Choose language:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    lang = call.data.split('_')[1]
    current_lang[call.from_user.id] = lang
    bot.answer_callback_query(call.id)
    show_catalog(call.message)

def show_catalog(message):
    text = get_text(message.chat.id, 'catalog')
    for k, p in PRODUCTS.items():
        text += f"{k}. {p[current_lang.get(message.chat.id, 'ru')]} — {p['price']} USDT\n"
    markup = InlineKeyboardMarkup(row_width=1)
    for k, p in PRODUCTS.items():
        markup.add(InlineKeyboardButton(f"{k}. {p[current_lang.get(message.chat.id, 'ru')]}", callback_data=f"buy_{k}"))
    bot.send_message(message.chat.id, text + "\n" + get_text(message.chat.id, 'choose'), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def buy_callback(call):
    num = call.data.split('_')[1]
    p = PRODUCTS[num]
    lang = current_lang.get(call.from_user.id, 'ru')
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 
        f"✅ Вы выбрали: {p[lang]}\n\nОплата: {p['price']} USDT (TRC20)\nПереведи на:\n{CRYPTO_WALLET}\n\nПосле оплаты напиши «ОПЛАТИЛ {num}»")

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
            bot.reply_to(message, "🎉 Оплата подтверждена! Отправляю товар...")
            try:
                with open(p['file'], "rb") as f:
                    bot.send_document(message.chat.id, f, caption=f"Вот твой товар: {p[current_lang.get(message.chat.id, 'ru')]}")
                bot.send_message(ADMIN_ID, f"🎉 Продажа! {p['ru']} за {p['price']} USDT")
            except:
                bot.reply_to(message, "Файл готов, но ошибка отправки. Напиши @Volodya")
        except:
            bot.reply_to(message, "Напиши «ОПЛАТИЛ X»")

print("🚀 Бот с кнопками и языками запущен")
bot.infinity_polling()
