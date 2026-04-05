import os
import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CRYPTO_WALLET = os.getenv('CRYPTO_WALLET')
ADMIN_ID = int(os.getenv('ADMIN_CHAT_ID'))

bot = telebot.TeleBot(TELEGRAM_TOKEN)

current_lang = {}

PRODUCTS = {
    "1": {"ru": "Готовый бот для авто-продаж", "en": "Ready sales bot", "price": 25, "file": "sales_bot.py",
          "teaser_ru": "Тизер: Этот бот автоматически показывает каталог, принимает оплату и выдаёт товары 24/7. Полный код — после оплаты."},
    "2": {"ru": "100 промптов Grok-OMEGA", "en": "100 Grok-OMEGA prompts", "price": 12, "file": "prompts.txt",
          "teaser_ru": "Тизер: 100 самых мощных промптов для бизнеса и заработка. Полный список — после оплаты."},
    "3": {"ru": "Арбитраж-бот", "en": "Arbitrage bot", "price": 37, "file": "arbitrage_bot.py",
          "teaser_ru": "Тизер: Автоматически ищет разницу цен на биржах. Полный код — после оплаты."},
    "4": {"ru": "TikTok Автопостинг бот", "en": "TikTok Auto-Poster Bot", "price": 59, "file": "tiktok_bot.py",
          "teaser_ru": "Тизер: Публикует видео в TikTok каждые 4 часа без твоего участия. Полный код — после оплаты."},
    "5": {"ru": "Продвинутая воронка продаж", "en": "Advanced Sales Funnel", "price": 49, "file": "funnel_bot.py",
          "teaser_ru": "Тизер: 5-шаговая воронка, которая ведёт клиента до оплаты. Полная настройка — после оплаты."},
    "6": {"ru": "Faceless Content Pack", "en": "Faceless Content Pack", "price": 39, "file": "faceless_pack.txt",
          "teaser_ru": "Тизер: 50 готовых идей контента без лица. Полный пак — после оплаты."},
    "7": {"ru": "Lead Generation Bot", "en": "Lead Generation Bot", "price": 35, "file": "lead_bot.py",
          "teaser_ru": "Тизер: Автоматически собирает контакты из чатов. Полный код — после оплаты."},
    "8": {"ru": "Passive Income Blueprint", "en": "Passive Income Blueprint", "price": 27, "file": "blueprint.txt",
          "teaser_ru": "Тизер: Пошаговый план пассивного дохода от 1000$ в месяц. Полный blueprint — после оплаты."}
}

def check_payment(txid, expected_amount):
    try:
        url = f"https://apilist.tronscanapi.com/api/transaction?hash={txid}"
        data = requests.get(url, timeout=10).json()
        if not data or not data.get('data'):
            return False, "Транзакция не найдена"
        tx = data['data'][0]
        amount = tx.get('amount', 0) / 1000000
        to_address = tx.get('to', '')
        if amount >= expected_amount - 1 and CRYPTO_WALLET.lower() in to_address.lower():
            return True, f"✅ Оплата {amount} USDT подтверждена"
        return False, "Сумма или адрес не совпадают"
    except:
        return False, "Ошибка проверки TXID. Попробуй ещё раз."

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
        text += f"{k}. {p[lang]} — ${p['price']}\n"
        markup.add(InlineKeyboardButton(f"{k}. {p[lang]}", callback_data=f"buy_{k}"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def buy_callback(call):
    num = call.data.split('_')[1]
    p = PRODUCTS[num]
    lang = current_lang.get(call.from_user.id, 'ru')
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, p['teaser_ru'] if lang == 'ru' else p['teaser_en'])
    bot.send_message(call.message.chat.id,
        "✅ Вы выбрали: " + p[lang] if lang == 'ru' else "✅ You chose: " + p[lang])
    bot.send_message(call.message.chat.id,
        "Оплата: $" + str(p['price']) + " USDT (TRC20)" if lang == 'ru' else "Payment: $" + str(p['price']) + " USDT (TRC20)")
    bot.send_message(call.message.chat.id, "Переведи на:\n" + CRYPTO_WALLET if lang == 'ru' else "Send to:\n" + CRYPTO_WALLET)
    bot.send_message(call.message.chat.id, "После оплаты пришли TXID транзакции")

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
            bot.reply_to(message, "Пришли TXID транзакции")
            bot.register_next_step_handler(message, lambda m2: process_tx(m2, num))
        except:
            bot.reply_to(message, "Напиши «ОПЛАТИЛ X»")
    else:
        bot.reply_to(message, "Напиши /catalog")

def process_tx(message, num):
    txid = message.text.strip()
    p = PRODUCTS[num]
    lang = current_lang.get(message.chat.id, 'ru')
    bot.reply_to(message, "🔍 Проверяю оплату...")
    success, msg = check_payment(txid, p['price'])
    if success:
        bot.reply_to(message, msg)
        try:
            with open(p['file'], "rb") as f:
                bot.send_document(message.chat.id, f, caption="🎉 Вот твой полный товар: " + p[lang])
            bot.send_message(ADMIN_ID, "🎉 Продажа! " + p['ru'] + " за $" + str(p['price']) + " USDT")
        except:
            bot.reply_to(message, "Файл готов, но ошибка отправки. Напиши @Volodya")
    else:
        bot.reply_to(message, msg + "\nПроверь TXID и попробуй ещё раз.")

print("🚀 Бот с автоматической проверкой оплаты запущен")
bot.infinity_polling()
