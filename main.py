import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CRYPTO_WALLET = os.getenv('CRYPTO_WALLET')
ADMIN_ID = int(os.getenv('ADMIN_CHAT_ID'))
SUPPORT_USERNAME = os.getenv('SUPPORT_USERNAME', '@Volodya')   # ← здесь твой username

bot = telebot.TeleBot(TELEGRAM_TOKEN)

current_lang = {}

PRODUCTS = {
    "1": {"ru": "Готовый бот для авто-продаж", "en": "Ready sales bot", "price": 25, "file": "sales_bot.py",
          "teaser_ru": "🔹 Тизер: Этот бот автоматически показывает каталог, принимает оплату и выдаёт товары 24/7. Полный код — после оплаты.",
          "teaser_en": "🔹 Teaser: This bot automatically shows catalog, accepts payment and delivers products 24/7. Full code — after payment."},
    "2": {"ru": "100 промптов Grok-OMEGA", "en": "100 Grok-OMEGA prompts", "price": 12, "file": "prompts.txt",
          "teaser_ru": "🔹 Тизер: 100 самых мощных промптов для бизнеса и заработка. Полный список — после оплаты.",
          "teaser_en": "🔹 Teaser: 100 most powerful prompts for business and earnings. Full list — after payment."},
    "3": {"ru": "Арбитраж-бот", "en": "Arbitrage bot", "price": 37, "file": "arbitrage_bot.py",
          "teaser_ru": "🔹 Тизер: Автоматически ищет разницу цен на биржах. Полный код — после оплаты.",
          "teaser_en": "🔹 Teaser: Automatically finds price differences on exchanges. Full code — after payment."},
    "4": {"ru": "TikTok Автопостинг бот", "en": "TikTok Auto-Poster Bot", "price": 59, "file": "tiktok_bot.py",
          "teaser_ru": "🔹 Тизер: Публикует видео в TikTok каждые 4 часа без твоего участия. Полный код — после оплаты.",
          "teaser_en": "🔹 Teaser: Posts videos to TikTok every 4 hours without your involvement. Full code — after payment."},
    "5": {"ru": "Продвинутая воронка продаж", "en": "Advanced Sales Funnel", "price": 49, "file": "funnel_bot.py",
          "teaser_ru": "🔹 Тизер: 5-шаговая воронка, которая ведёт клиента до оплаты. Полная настройка — после оплаты.",
          "teaser_en": "🔹 Teaser: 5-step funnel that guides the client to payment. Full setup — after payment."},
    "6": {"ru": "Faceless Content Pack", "en": "Faceless Content Pack", "price": 39, "file": "faceless_pack.txt",
          "teaser_ru": "🔹 Тизер: 50 готовых идей контента без лица. Полный пак — после оплаты.",
          "teaser_en": "🔹 Teaser: 50 ready faceless content ideas. Full pack — after payment."},
    "7": {"ru": "Lead Generation Bot", "en": "Lead Generation Bot", "price": 35, "file": "lead_bot.py",
          "teaser_ru": "🔹 Тизер: Автоматически собирает контакты из чатов. Полный код — после оплаты.",
          "teaser_en": "🔹 Teaser: Automatically collects contacts from chats. Full code — after payment."},
    "8": {"ru": "Passive Income Blueprint", "en": "Passive Income Blueprint", "price": 27, "file": "blueprint.txt",
          "teaser_ru": "🔹 Тизер: Пошаговый план пассивного дохода от 1000$ в месяц. Полный blueprint — после оплаты.",
          "teaser_en": "🔹 Teaser: Step-by-step passive income plan from $1000 per month. Full blueprint — after payment."}
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
                bot.reply_to(message, "Файл готов, но ошибка отправки. Напиши " + SUPPORT_USERNAME)
        except:
            bot.reply_to(message, "Напиши \"ОПЛАТИЛ X\"" if current_lang.get(message.chat.id, 'ru') == 'ru' else "Write \"PAID X\"")
    else:
        bot.reply_to(message, "Напиши /catalog")

print("🚀 Бот с твоим username в ошибке запущен")
bot.infinity_polling()
