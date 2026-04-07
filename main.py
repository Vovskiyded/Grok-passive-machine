import os
import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CRYPTO_WALLET = os.getenv('CRYPTO_WALLET')
ADMIN_ID = int(os.getenv('ADMIN_CHAT_ID'))

bot = telebot.TeleBot(TELEGRAM_TOKEN)

current_lang = {}
pending_tx = {}

PRODUCTS = {
    "1": {"ru": "Автоматизация бизнеса (20 кодов)", "en": "Business Automation (20 codes)", "ua": "Автоматизація бізнесу (20 кодів)",
          "es": "Automatización de negocios (20 códigos)", "ar": "أتمتة الأعمال (20 كود)", "fr": "Automatisation d'entreprise (20 codes)",
          "price": 39, "file": "automation_codes.txt",
          "teaser_ru": "20 готовых кодов, которые полностью автоматизируют продажи, сбор лидов, постинг, парсинг цен конкурентов и генерацию отчётов. Каждый код идёт с подробной инструкцией. Полная версия — после оплаты."},
    "2": {"ru": "Коды + подробные инструкции (20 наборов)", "en": "Codes + Instructions (20 sets)", "ua": "Коди + інструкції (20 наборів)",
          "es": "Códigos + instrucciones detalladas (20 conjuntos)", "ar": "أكواد + تعليمات مفصلة (20 مجموعة)", "fr": "Codes + instructions détaillées (20 ensembles)",
          "price": 49, "file": "code_instructions.txt",
          "teaser_ru": "20 полных наборов: готовый код + максимально подробная пошаговая инструкция на 10–15 шагов. Идеально даже для полного новичка. Полная версия — после оплаты."},
    "3": {"ru": "Удалённая работа и заработок", "en": "Remote Work & Earning", "ua": "Віддалена робота та заробіток",
          "es": "Trabajo remoto y ganancias", "ar": "العمل عن بعد والكسب", "fr": "Travail à distance et revenus",
          "price": 24.99, "file": "remote_earning.txt",
          "teaser_ru": "Благодаря ИИ не обязательно быть программистом или айтишником, чтобы зарабатывать хорошие деньги. Главное — решимость и желание зарабатывать. Полный гайд по реальным способам дистанционного заработка — после оплаты."},
    "4": {"ru": "Grok Промпт Арсенал 100", "en": "Grok Prompt Arsenal 100", "ua": "Grok Промпт Арсенал 100",
          "es": "Grok Prompt Arsenal 100", "ar": "Grok Prompt Arsenal 100", "fr": "Grok Prompt Arsenal 100",
          "price": 9, "file": "prompts.txt",
          "teaser_ru": "100 самых мощных промптов Grok-OMEGA для бизнеса, контента, продаж и заработка. Полный список — после оплаты."},
    "5": {"ru": "Grok TikTok Rocket", "en": "Grok TikTok Rocket", "ua": "Grok TikTok Rocket",
          "es": "Grok TikTok Rocket", "ar": "Grok TikTok Rocket", "fr": "Grok TikTok Rocket",
          "price": 49, "file": "tiktok_bot.py",
          "teaser_ru": "Бот, который полностью берёт на себя продвижение в TikTok: сам добавляет текст и публикует faceless-видео каждые 4 часа. Полный код — после оплаты."},
    "6": {"ru": "Grok Арбитраж Скалпер", "en": "Grok Arbitrage Scalper", "ua": "Grok Арбитраж Скалпер",
          "es": "Grok Arbitrage Scalper", "ar": "Grok Arbitrage Scalper", "fr": "Grok Arbitrage Scalper",
          "price": 29, "file": "arbitrage_bot.py",
          "teaser_ru": "Автоматический поиск разницы цен на биржах в реальном времени. Полный код — после оплаты."},
    "7": {"ru": "Grok Безликая Фабрика", "en": "Grok Faceless Factory", "ua": "Grok Безликая Фабрика",
          "es": "Grok Fabrica Sin Rostro", "ar": "Grok مصنع بدون وجه", "fr": "Grok Usine Sans Visage",
          "price": 29, "file": "faceless_pack.txt",
          "teaser_ru": "50 готовых идей faceless-контента + шаблоны. Полный пак — после оплаты."},
    "8": {"ru": "Grok Lead Hunter", "en": "Grok Lead Hunter", "ua": "Grok Lead Hunter",
          "es": "Grok Lead Hunter", "ar": "Grok Lead Hunter", "fr": "Grok Lead Hunter",
          "price": 25, "file": "lead_bot.py",
          "teaser_ru": "Автоматический сбор тёплых лидов из чатов. Полный код — после оплаты."},
    "9": {"ru": "Grok Passive Blueprint", "en": "Grok Passive Blueprint", "ua": "Grok Passive Blueprint",
          "es": "Grok Passive Blueprint", "ar": "Grok Passive Blueprint", "fr": "Grok Passive Blueprint",
          "price": 19, "file": "blueprint.txt",
          "teaser_ru": "Пошаговый план запуска пассивного дохода от 1000$ в месяц. Полный blueprint — после оплаты."},
    "10": {"ru": "Grok Воронка Pro", "en": "Grok Funnel Pro", "ua": "Grok Воронка Pro",
           "es": "Grok Funnel Pro", "ar": "Grok Funnel Pro", "fr": "Grok Funnel Pro",
           "price": 35, "file": "funnel_bot.py",
           "teaser_ru": "5-шаговая продающая воронка, которая ведёт клиента до оплаты. Полная настройка — после оплаты."},
    "11": {"ru": "Купить номер для Telegram / WhatsApp", "en": "Buy Telegram / WhatsApp Number", "ua": "Купити номер для Telegram / WhatsApp",
           "es": "Comprar número para Telegram / WhatsApp", "ar": "شراء رقم لـ Telegram / WhatsApp", "fr": "Acheter un numéro pour Telegram / WhatsApp",
           "price": 24, "file": "numbers_pack.txt",
           "teaser_ru": "Покупка прогретых номеров для регистрации Telegram и WhatsApp. 24$ на месяц или 88$ на год. Актуальные номера с хорошей историей. Заказ через поддержку — после оплаты."}
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("Русский", callback_data="lang_ru"))
    markup.add(InlineKeyboardButton("English", callback_data="lang_en"))
    markup.add(InlineKeyboardButton("Español", callback_data="lang_es"))
    markup.add(InlineKeyboardButton("العربية", callback_data="lang_ar"))
    markup.add(InlineKeyboardButton("Français", callback_data="lang_fr"))
    bot.reply_to(message, "Привет! 👋\n\nВ каждом паке есть готовые инструменты и подробная инструкция.\nТолько выберите для себя направление.\n\nВыбери язык:", reply_markup=markup)

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
        markup.add(InlineKeyboardButton(f"{k}. {p[lang]} — ${p['price']}", callback_data=f"buy_{k}"))
    markup.add(InlineKeyboardButton("Поддержка", url="https://t.me/grom_ii"))
    markup.add(InlineKeyboardButton("О нашей компании", callback_data="about"))
    markup.add(InlineKeyboardButton("Политика конфиденциальности", callback_data="privacy"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def buy_callback(call):
    num = call.data.split('_')[1]
    p = PRODUCTS[num]
    lang = current_lang.get(call.from_user.id, 'ru')
    bot.answer_callback_query(call.id)
    teaser = p['teaser_ru'] if lang == 'ru' else p.get('teaser_en', p['teaser_ru'])
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("💰 Купить за $" + str(p['price']), callback_data=f"paymenu_{num}"))
    bot.send_message(call.message.chat.id, teaser, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('paymenu_'))
def pay_menu(call):
    num = call.data.split('_')[1]
    p = PRODUCTS[num]
    lang = current_lang.get(call.from_user.id, 'ru')
    bot.answer_callback_query(call.id)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("💎 USDT TRC20", callback_data=f"pay_usdt_{num}"))
    markup.add(InlineKeyboardButton("💳 Другие способы оплаты", callback_data=f"pay_card_{num}"))
    bot.send_message(call.message.chat.id, "Выберите способ оплаты:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def payment_choice(call):
    action, num = call.data.split('_')[1:]
    if action == "usdt":
        bot.send_message(call.message.chat.id, "Оплата: $" + str(PRODUCTS[num]['price']) + " USDT (TRC20)\nПереведи на:\n" + CRYPTO_WALLET + "\n\nПосле оплаты пришли TXID")
        pending_tx[call.from_user.id] = num
    else:
        bot.send_message(call.message.chat.id, "Оплата другими способами:\n@grom_ii\n\nПосле оплаты напиши «ОПЛАТИЛ " + num + "»")
        pending_tx[call.from_user.id] = num

@bot.message_handler(func=lambda m: True)
def handle(message):
    text = message.text.strip()
    user_id = message.chat.id
    if user_id in pending_tx:
        num = pending_tx[user_id]
        p = PRODUCTS[num]
        lang = current_lang.get(user_id, 'ru')
        bot.reply_to(message, "🔍 Проверяю оплату...")
        success, msg = check_trx(text, p['price'])
        if success:
            bot.reply_to(message, msg)
            try:
                with open(p['file'], "rb") as f:
                    bot.send_document(message.chat.id, f, caption="🎉 Вот твой полный товар:")
                bot.send_message(ADMIN_ID, "🎉 Продажа! " + p['ru'] + " за $" + str(p['price']) + " USDT")
            except:
                bot.reply_to(message, "Файл готов, но ошибка отправки. Напиши @grom_ii")
            del pending_tx[user_id]
        else:
            bot.reply_to(message, msg + "\nПроверь TXID и попробуй ещё раз.")
    else:
        bot.reply_to(message, "Напиши /start")

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

print("🚀 Бот запущен")
bot.infinity_polling()
