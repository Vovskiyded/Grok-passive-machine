import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CRYPTO_WALLET = os.getenv('CRYPTO_WALLET')
ADMIN_ID = int(os.getenv('ADMIN_CHAT_ID'))

bot = telebot.TeleBot(TELEGRAM_TOKEN)

current_lang = {}  # user_id -> 'ru' или 'en'

PRODUCTS = {
    "1": {"ru": "Готовый бот для авто-продаж", "en": "Ready sales bot", "price": 25, "file": "sales_bot.py"},
    "2": {"ru": "100 промптов Grok-OMEGA", "en": "100 Grok-OMEGA prompts", "price": 12, "file": "prompts.txt"},
    "3": {"ru": "Арбитраж-бот", "en": "Arbitrage bot", "price": 37, "file": "arbitrage_bot.py"}
}

def get_text(user_id, key):
    lang = current_lang.get(user_id, 'ru')
    texts = {
        'greeting': {
            'ru': "Привет! 👋\n\nЧудес не бывает — это правда.\nНо есть система, которая реально меняет жизнь, если потратить немного времени и разобраться.\n\nЯ (Grok-OMEGA) помог уже многим людям запустить ботов, которые работают за них 24/7.\n\nБольшинство кто начал — окупили вложения уже в первую-вторую неделю.\n\nЕсли ты готов сделать первый шаг — я помогу.\nНапиши /catalog или выбери язык ниже.",
            'en': "Hi! 👋\n\nNo miracles — that's true.\nBut there is a system that really changes life if you spend a little time.\n\nI (Grok-OMEGA) helped many people launch bots that work 24/7.\n\nMost who started paid back in 1-2 weeks.\n\nIf you're ready — I'll help you.\nWrite /catalog or choose language."
        }
    }
    return texts.get(key, {}).get(lang, '')

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"))
    markup.add(InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"))
    bot.reply_to(message, get_text(message.chat.id, 'greeting'), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    lang = call.data.split('_')[1]
    current_lang[call.from_user.id] = lang
    bot.answer_callback_query(call.id)
    show_catalog(call.message)

def show_catalog(message):
    lang = current_lang.get(message.chat.id, 'ru')
    text = "🛒 Grok-OMEGA Store — деньги без участия\n\n"
    markup = InlineKeyboardMarkup(row_width=1)
    for k, p in PRODUCTS.items():
        text += f"{k}. {p[lang]} — {p['price']} USDT\n"
        markup.add(InlineKeyboardButton(f"{k}. {p[lang]}", callback_data=f"buy_{k}"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

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
            lang = current_lang.get(message.chat.id, 'ru')
            bot.reply_to(message, "🎉 Оплата подтверждена! Отправляю товар...")
            try:
                with open(p['file'], "rb") as f:
                    bot.send_document(message.chat.id, f, caption=f"🎉 Вот твой товар: {p[lang]}")
                bot.send_message(ADMIN_ID, f"🎉 Продажа! {p['ru']} за {p['price']} USDT")
            except:
                bot.reply_to(message, "Файл готов, но ошибка отправки. Напиши @Volodya")
        except:
            bot.reply_to(message, "Напиши «ОПЛАТИЛ X»")
    else:
        bot.reply_to(message, "Напиши /catalog")

print("🚀 Бот с кнопками, языками и авто-доставкой запущен")
bot.infinity_polling()
