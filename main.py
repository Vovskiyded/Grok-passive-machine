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
          "teaser_ru": "🔹 Тизер: Представь, что твой Telegram-бот работает 24/7 без твоего участия. Он сам показывает каталог, принимает оплату и мгновенно выдаёт товары клиентам. Это готовая система авто-продаж, которая уже приносит деньги сотням людей. Полный код и настройка — сразу после оплаты."},
    "2": {"ru": "100 промптов Grok-OMEGA", "en": "100 Grok-OMEGA prompts", "price": 12, "file": "prompts.txt",
          "teaser_ru": "🔹 Тизер: 100 самых мощных промптов, которые позволяют за секунды генерировать продающий контент, идеи бизнеса и автоматизацию. Вот первые 5 примеров (полный список 100 промптов — сразу после оплаты)."},
    "3": {"ru": "Арбитраж-бот", "en": "Arbitrage bot", "price": 37, "file": "arbitrage_bot.py",
          "teaser_ru": "🔹 Тизер: Этот бот автоматически мониторит биржи и находит разницу в ценах, показывая тебе готовые возможности для арбитража. Работает на любом капитале. Полный код и настройка — сразу после оплаты."},
    "4": {"ru": "TikTok Автопостинг бот", "en": "TikTok Auto-Poster Bot", "price": 59, "file": "tiktok_bot.py",
          "teaser_ru": "🔹 Тизер: Бот сам генерирует видео, текст и публикует посты в TikTok каждые 4 часа. Ты просто загружаешь стоковое видео и отдыхаешь. Полный код — сразу после оплаты."},
    "5": {"ru": "Продвинутая воронка продаж", "en": "Advanced Sales Funnel", "price": 49, "file": "funnel_bot.py",
          "teaser_ru": "🔹 Тизер: 5-шаговая воронка, которая автоматически приветствует клиента, показывает каталог, принимает оплату и выдаёт товар. Полная настройка и готовый код — сразу после оплаты."},
    "6": {"ru": "Faceless Content Pack", "en": "Faceless Content Pack", "price": 39, "file": "faceless_pack.txt",
          "teaser_ru": "🔹 Тизер: 50 готовых идей контента без лица + шаблоны видео и текстов. Идеально для тех, кто хочет зарабатывать на TikTok и YouTube без камеры. Полный пак с 200+ материалами — сразу после оплаты."},
    "7": {"ru": "Lead Generation Bot", "en": "Lead Generation Bot", "price": 35, "file": "lead_bot.py",
          "teaser_ru": "🔹 Тизер: Бот автоматически собирает контакты клиентов из чатов и каналов. Ты получаешь базу лидов, которые уже заинтересованы в твоём продукте. Полный код с парсингом — сразу после оплаты."},
    "8": {"ru": "Passive Income Blueprint", "en": "Passive Income Blueprint", "price": 27, "file": "blueprint.txt",
          "teaser_ru": "🔹 Тизер: Пошаговый план запуска пассивного дохода от 1000$ в месяц. С шаблонами, чек-листами и примерами. Полный blueprint — сразу после оплаты."}
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
    teaser = p['teaser_ru'] if lang == 'ru' else p['teaser_en']
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, teaser)
    bot.send_message(call.message.chat.id, "✅ Вы выбрали: " + p[lang] if lang == 'ru' else "✅ You chose: " + p[lang])
    bot.send_message(call.message.chat.id, "Оплата: $" + str(p['price']) + " USDT (TRC20)" if lang == 'ru' else "Payment: $" + str(p['price']) + " USDT (TRC20)")
    bot.send_message(call.message.chat.id, "Переведи на:\n" + CRYPTO_WALLET if lang == 'ru' else "Send to:\n" + CRYPTO_WALLET)
    bot.send_message(call.message.chat.id, "После оплаты напиши \"ОПЛАТИЛ " + num + "\"" if lang == 'ru' else "After payment write \"PAID " + num + "\"")

@bot.message_handler(func=lambda m: True)
def handle(message):
    text = message.text.strip().upper()
    if "ОПЛАТИЛ" in text or "PAID" in text:
        try:
            num = text.split()[1]
            if num not in PRODUCTS:
                bot.reply_to(message, "Неверный номер" if current_lang.get(message.chat.id, 'ru') == 'ru' else "Invalid number")
                return
            p = PRODUCTS[num]
            lang = current_lang.get(message.chat.id, 'ru')
            bot.reply_to(message, "🎉 Оплата подтверждена! Отправляю полный товар..." if lang == 'ru' else "🎉 Payment confirmed! Sending full product...")
            try:
                with open(p['file'], "rb") as f:
                    bot.send_document(message.chat.id, f, caption="🎉 Вот твой полный товар: " + p[lang] if lang == 'ru' else "🎉 Your full product: " + p[lang])
                bot.send_message(ADMIN_ID, "🎉 Продажа! " + p['ru'] + " за $" + str(p['price']) + " USDT")
            except:
                bot.reply_to(message, "Файл готов, но ошибка отправки. Напиши @Volodya")
        except:
            bot.reply_to(message, "Напиши \"ОПЛАТИЛ X\"" if current_lang.get(message.chat.id, 'ru') == 'ru' else "Write \"PAID X\"")
    else:
        bot.reply_to(message, "Напиши /catalog")

print("🚀 Бот с развернутыми тизерами запущен")
bot.infinity_polling()
