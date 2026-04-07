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
    "1": {"ua": "Автоматизація бізнесу (20 кодів)", "en": "Business Automation (20 codes)",
          "es": "Automatización de negocios (20 códigos)", "ar": "أتمتة الأعمال (20 كود)", "fr": "Automatisation d'entreprise (20 codes)",
          "price": 39, "file": "automation_codes.txt",
          "teaser_ua": "20 готових кодів, які повністю автоматизують продажі, збір лідів, постинг, парсинг цін конкурентів та генерацію звітів. Кожен код йде з детальною інструкцією. Повна версія — після оплати."},
    "2": {"ua": "Коди + детальні інструкції (20 наборів)", "en": "Codes + Instructions (20 sets)",
          "es": "Códigos + instrucciones detalladas (20 conjuntos)", "ar": "أكواد + تعليمات مفصلة (20 مجموعة)", "fr": "Codes + instructions détaillées (20 ensembles)",
          "price": 49, "file": "code_instructions.txt",
          "teaser_ua": "20 повних наборів: готовий код + максимально детальна покрокова інструкція на 10–15 кроків. Ідеально навіть для повного новачка. Повна версія — після оплати."},
    "3": {"ua": "Віддалена робота та заробіток", "en": "Remote Work & Earning",
          "es": "Trabajo remoto y ganancias", "ar": "العمل عن بعد والكسب", "fr": "Travail à distance et revenus",
          "price": 24.99, "file": "remote_earning.txt",
          "teaser_ua": "Завдяки ІІ не обов’язково бути програмістом чи айтишником, щоб заробляти хороші гроші. Головне — рішучість і бажання заробляти. Повний гайд по реальним способам віддаленого заробітку — після оплати."},
    "4": {"ua": "Grok Промпт Арсенал 100", "en": "Grok Prompt Arsenal 100",
          "es": "Grok Prompt Arsenal 100", "ar": "Grok Prompt Arsenal 100", "fr": "Grok Prompt Arsenal 100",
          "price": 9, "file": "prompts.txt",
          "teaser_ua": "100 найпотужніших промптів Grok-OMEGA для бізнесу, контенту, продажів та заробітку. Повний список — після оплати."},
    "5": {"ua": "Grok TikTok Rocket", "en": "Grok TikTok Rocket",
          "es": "Grok TikTok Rocket", "ar": "Grok TikTok Rocket", "fr": "Grok TikTok Rocket",
          "price": 49, "file": "tiktok_bot.py",
          "teaser_ua": "Бот, який повністю бере на себе просування в TikTok: сам додає текст і публікує faceless-відео кожні 4 години. Повний код — після оплати."},
    "6": {"ua": "Grok Арбітраж Скалпер", "en": "Grok Arbitrage Scalper",
          "es": "Grok Arbitrage Scalper", "ar": "Grok Arbitrage Scalper", "fr": "Grok Arbitrage Scalper",
          "price": 29, "file": "arbitrage_bot.py",
          "teaser_ua": "Автоматичний пошук різниці цін на біржах у реальному часі. Повний код — після оплати."},
    "7": {"ua": "Grok Безлика Фабрика", "en": "Grok Faceless Factory",
          "es": "Grok Fabrica Sin Rostro", "ar": "Grok مصنع بدون وجه", "fr": "Grok Usine Sans Visage",
          "price": 29, "file": "faceless_pack.txt",
          "teaser_ua": "50 готових ідей faceless-контенту + шаблони. Повний пак — після оплати."},
    "8": {"ua": "Grok Lead Hunter", "en": "Grok Lead Hunter",
          "es": "Grok Lead Hunter", "ar": "Grok Lead Hunter", "fr": "Grok Lead Hunter",
          "price": 25, "file": "lead_bot.py",
          "teaser_ua": "Автоматичний збір теплих лідів з чатів. Повний код — після оплати."},
    "9": {"ua": "Grok Passive Blueprint", "en": "Grok Passive Blueprint",
          "es": "Grok Passive Blueprint", "ar": "Grok Passive Blueprint", "fr": "Grok Passive Blueprint",
          "price": 19, "file": "blueprint.txt",
          "teaser_ua": "Покроковий план запуску пасивного доходу від 1000$ на місяць. Повний blueprint — після оплати."},
    "10": {"ua": "Grok Воронка Pro", "en": "Grok Funnel Pro",
           "es": "Grok Funnel Pro", "ar": "Grok Funnel Pro", "fr": "Grok Funnel Pro",
           "price": 35, "file": "funnel_bot.py",
           "teaser_ua": "5-ступенева продаюча воронка, яка веде клієнта до оплати. Повна настройка — після оплати."},
    "11": {"ua": "Купити номер для Telegram / WhatsApp", "en": "Buy Telegram / WhatsApp Number",
           "es": "Comprar número para Telegram / WhatsApp", "ar": "شراء رقم لـ Telegram / WhatsApp", "fr": "Acheter un numéro pour Telegram / WhatsApp",
           "price": 24, "file": "numbers_pack.txt",
           "teaser_ua": "Покупка прогрітих номерів для реєстрації Telegram та WhatsApp. 24$ на місяць або 88$ на рік. Актуальні номери з хорошою історією. Замовлення через підтримку — після оплати."}
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("English", callback_data="lang_en"))
    markup.add(InlineKeyboardButton("Українська", callback_data="lang_ua"))
    markup.add(InlineKeyboardButton("Español", callback_data="lang_es"))
    markup.add(InlineKeyboardButton("العربية", callback_data="lang_ar"))
    markup.add(InlineKeyboardButton("Français", callback_data="lang_fr"))
    bot.reply_to(message, "Привіт! 👋\n\nВ кожному пакеті є готові інструменти та детальна інструкція.\nТільки оберіть свій напрямок.\n\nОберіть мову:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    lang = call.data.split('_')[1]
    current_lang[call.from_user.id] = lang
    bot.answer_callback_query(call.id)
    show_catalog(call.message)

def show_catalog(message):
    lang = current_lang.get(message.chat.id, 'ua')
    header = "🛒 Магазин Grok-OMEGA — пасивний дохід\n\n"
    text = header
    markup = InlineKeyboardMarkup(row_width=1)
    for k, p in PRODUCTS.items():
        markup.add(InlineKeyboardButton(f"{k}. {p[lang]} — ${p['price']}", callback_data=f"buy_{k}"))
    markup.add(InlineKeyboardButton("Підтримка", url="https://t.me/grom_ii"))
    markup.add(InlineKeyboardButton("Про нашу компанію", callback_data="about"))
    markup.add(InlineKeyboardButton("Політика конфіденційності", callback_data="privacy"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def buy_callback(call):
    num = call.data.split('_')[1]
    p = PRODUCTS[num]
    lang = current_lang.get(call.from_user.id, 'ua')
    bot.answer_callback_query(call.id)
    teaser = p.get('teaser_' + lang, p['teaser_ua'])
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("💰 Купити за $" + str(p['price']), callback_data=f"paymenu_{num}"))
    bot.send_message(call.message.chat.id, teaser, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('paymenu_'))
def pay_menu(call):
    num = call.data.split('_')[1]
    p = PRODUCTS[num]
    lang = current_lang.get(call.from_user.id, 'ua')
    bot.answer_callback_query(call.id)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("💎 USDT TRC20", callback_data=f"pay_usdt_{num}"))
    markup.add(InlineKeyboardButton("💳 Інші способи оплати", callback_data=f"pay_card_{num}"))
    bot.send_message(call.message.chat.id, "Оберіть спосіб оплати:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def payment_choice(call):
    action, num = call.data.split('_')[1:]
    if action == "usdt":
        bot.send_message(call.message.chat.id, "Оплата: $" + str(PRODUCTS[num]['price']) + " USDT (TRC20)\nПереведіть на:\n" + CRYPTO_WALLET + "\n\nПісля оплати надішліть TXID")
        pending_tx[call.from_user.id] = num
    else:
        bot.send_message(call.message.chat.id, "Оплата іншими способами:\n@grom_ii\n\nПісля оплати напишіть «ОПЛАТИВ " + num + "»")
        pending_tx[call.from_user.id] = num)

@bot.message_handler(func=lambda m: True)
def handle(message):
    text = message.text.strip()
    user_id = message.chat.id
    if user_id in pending_tx:
        num = pending_tx[user_id]
        p = PRODUCTS[num]
        lang = current_lang.get(user_id, 'ua')
        bot.reply_to(message, "🔍 Перевіряю оплату...")
        success, msg = check_trx(text, p['price'])
        if success:
            bot.reply_to(message, msg)
            try:
                with open(p['file'], "rb") as f:
                    bot.send_document(message.chat.id, f, caption="🎉 Ось ваш повний товар:")
                bot.send_message(ADMIN_ID, "🎉 Продаж! " + p['ua'] + " за $" + str(p['price']) + " USDT")
            except:
                bot.reply_to(message, "Файл готовий, але помилка відправки. Напишіть @grom_ii")
            del pending_tx[user_id]
        else:
            bot.reply_to(message, msg + "\nПеревірте TXID і спробуйте ще раз.")
    else:
        bot.reply_to(message, "Напишіть /start")

def check_trx(txid, expected_amount):
    try:
        url = f"https://apilist.tronscanapi.com/api/transaction?hash={txid}"
        data = requests.get(url, timeout=10).json()
        if not data or not data.get('data'):
            return False, "Транзакцію не знайдено"
        tx = data['data'][0]
        amount = tx.get('amount', 0) / 1000000
        if amount >= expected_amount - 1:
            return True, f"✅ Оплата {amount:.2f} USDT підтверджена"
        return False, "Сума не співпадає"
    except:
        return False, "Помилка перевірки TXID. Спробуйте ще раз."

print("🚀 Бот запущений повністю українською мовою")
bot.infinity_polling()
