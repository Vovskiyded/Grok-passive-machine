import os
import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CRYPTO_WALLET = os.getenv('CRYPTO_WALLET')
ADMIN_ID = int(os.getenv('ADMIN_CHAT_ID'))

bot = telebot.TeleBot(TELEGRAM_TOKEN)

current_lang = {}
pending_tx = {}  # user_id → product_num

PRODUCTS = {
    "1": {"ru": "Grok АвтоПродажник", "en": "Grok AutoSeller", "price": 25, "file": "sales_bot.py",
          "teaser_ru": "Тизер (30%): Бот сам показывает каталог, принимает оплату USDT и мгновенно выдаёт файлы. Пример: клиент выбирает товар №3 → бот пишет «ОПЛАТИЛ 3» → файл улетает автоматически. Полный код и настройка — после оплаты."},
    "2": {"ru": "Grok Промпт-Арсенал 100", "en": "Grok Prompt Arsenal 100", "price": 12, "file": "prompts.txt",
          "teaser_ru": "Тизер (30%): Вот 3 реальных промпта из 100: 1. «Напиши 10 вирусных идей TikTok для пассивного дохода». 2. «Создай бизнес-план на 30 дней с доходом 1000$». 3. «Составь 20 продающих постов для Telegram-канала». Полные 100 — после оплаты."},
    "3": {"ru": "Grok Арбитраж-Скалпер", "en": "Grok Arbitrage Scalper", "price": 37, "file": "arbitrage_bot.py",
          "teaser_ru": "Тизер (30%): Бот сканирует Binance + Bybit и показывает разницу. Пример: BTC 68450$ → 68720$ = +0.4% (270$ на 1 BTC). Полный код с автоматической торговлей — после оплаты."},
    "4": {"ru": "Grok TikTok Ракета", "en": "Grok TikTok Rocket", "price": 59, "file": "tiktok_bot.py",
          "teaser_ru": "Тизер (30%): Бот берёт stock.mp4, добавляет текст и публикует каждые 4 часа. Пример: 1 видео → 4 поста в сутки без тебя. Полный код + cookies + расписание — после оплаты."},
    "5": {"ru": "Grok Воронка Pro", "en": "Grok Funnel Pro", "price": 49, "file": "funnel_bot.py",
          "teaser_ru": "Тизер (30%): 5-шаговая воронка. Шаг 1: приветствие + тизер. Шаг 2: каталог. Шаг 3: оплата. Полная настройка под твой бот — после оплаты."},
    "6": {"ru": "Grok Безликая Фабрика", "en": "Grok Faceless Factory", "price": 39, "file": "faceless_pack.txt",
          "teaser_ru": "Тизер (30%): 3 готовые идеи из 50: 1. График «Один бот = 400$/мес» + текст. 2. «Как я запустил 20 ботов». 3. «Пассивный доход без лица». Полные 50 идей + шаблоны — после оплаты."},
    "7": {"ru": "Grok Охотник за Лидами", "en": "Grok Lead Hunter", "price": 35, "file": "lead_bot.py",
          "teaser_ru": "Тизер (30%): Бот автоматически собирает username + сообщения из любого чата. Пример: @user написал «интересно» → бот сохраняет контакт. Полный код — после оплаты."},
    "8": {"ru": "Grok Система Пассива", "en": "Grok Passive System", "price": 27, "file": "blueprint.txt",
          "teaser_ru": "Тизер (30%): Пошаговый план: 1. Выбрать нишу. 2. Создать бота. 3. Запустить на Railway. 4. Получать 1000$+/мес. Полный blueprint на 30+ страниц — после оплаты."},
    "9": {"ru": "Grok Запуск для Новичка", "en": "Grok Newbie Launchpad", "price": 19.99, "file": "beginner_guide.txt",
          "teaser_ru": "Тизер (30%): Полный гайд от А до Я. Шаги: BotFather → GitHub → Railway → Variables → Redeploy. Пример: как добавить TELEGRAM_TOKEN. Полная инструкция со всеми скриншотами и ссылками — после оплаты."}
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"))
    markup.add(InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"))
    bot.reply_to(message, 
        "Привет! 👋\n\n"
        "В каждом паке есть готовые инструменты и подробная инструкция к их использованию.\n"
        "Только выберите для себя направление.\n\n"
        "Выбери язык / Choose language:", 
        reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    lang = call.data.split('_')[1]
    current_lang[call.from_user.id] = lang
    bot.answer_callback_query(call.id)
    show_catalog(call.message)

def show_catalog(message):
    lang = current_lang.get(message.chat.id, 'ru')
    header = "🛒 Магазин Grok-OMEGA — пассивный доход\n\n" if lang == 'ru' else "🛒 Grok-OMEGA Store — passive income\n\n"
    text = header
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
    bot.send_message(call.message.chat.id, p['teaser_ru'] if lang == 'ru' else p.get('teaser_en', p['teaser_ru']))
    bot.send_message(call.message.chat.id, "✅ Вы выбрали: " + p[lang] if lang == 'ru' else "✅ You chose: " + p[lang])
    bot.send_message(call.message.chat.id, "Оплата: $" + str(p['price']) + " USDT (TRC20)" if lang == 'ru' else "Payment: $" + str(p['price']) + " USDT (TRC20)")
    bot.send_message(call.message.chat.id, "Переведи на:\n" + CRYPTO_WALLET if lang == 'ru' else "Send to:\n" + CRYPTO_WALLET)
    bot.send_message(call.message.chat.id, "После оплаты пришли TXID транзакции")
    pending_tx[call.from_user.id] = num   # ← СРАЗУ запоминаем товар

@bot.message_handler(func=lambda m: True)
def handle(message):
    text = message.text.strip()
    user_id = message.chat.id

    if user_id in pending_tx:                                 # ← Главное исправление
        num = pending_tx[user_id]
        p = PRODUCTS[num]
        lang = current_lang.get(user_id, 'ru')
        bot.reply_to(message, "🔍 Проверяю оплату...")
        success, msg = check_trx(text, p['price'])
        if success:
            bot.reply_to(message, msg)
            try:
                with open(p['file'], "rb") as f:
                    bot.send_document(message.chat.id, f, caption="🎉 Вот твой полный товар: " + p[lang])
                bot.send_message(ADMIN_ID, "🎉 Продажа! " + p['ru'] + " за $" + str(p['price']) + " USDT")
            except:
                bot.reply_to(message, "Файл готов, но ошибка отправки. Напиши @Volodya")
            del pending_tx[user_id]
        else:
            bot.reply_to(message, msg + "\nПроверь TXID и попробуй ещё раз.")
    elif "ОПЛАТИЛ" in text.upper():
        try:
            num = text.split()[1]
            if num not in PRODUCTS:
                bot.reply_to(message, "Неверный номер")
                return
            bot.reply_to(message, "Пришли TXID транзакции")
            pending_tx[message.chat.id] = num
        except:
            bot.reply_to(message, "Напиши «ОПЛАТИЛ X»")
    else:
        bot.reply_to(message, "Напиши /catalog")

def check_trx(txid, expected_amount):
    try:
        url = f"https://apilist.tronscanapi.com/api/transaction?hash={txid}"
        data = requests.get(url, timeout=10).json()
        if not data or not data.get('data'):
            return False, "Транзакция не найдена"
        tx = data['data'][0]
        amount = tx.get('amount', 0) / 1000000
        if amount >= expected_amount - 1:
            return True, f"✅ Оплата {amount:.2f} USDT подтверждена"
        return False, "Сумма не совпадает"
    except:
        return False, "Ошибка проверки TXID. Попробуй ещё раз."

print("🚀 Бот с мгновенной проверкой TXID запущен")
bot.infinity_polling()
