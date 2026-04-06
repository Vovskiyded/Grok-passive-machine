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
pending_product = {}

PRODUCTS = {
    "1": {"ru": "Автоматизация бизнеса (20 кодов)", "en": "Business Automation (20 codes)", "ua": "Автоматизація бізнесу (20 кодів)",
          "price": 49, "file": "automation_codes.txt",
          "teaser_ru": "Тизер (30%): 20 готовых кодов для автоматизации продаж, лидов, контента и рутины. Полный набор — после оплаты."},
    "2": {"ru": "Коды + инструкции (20 наборов)", "en": "Codes + Instructions (20 sets)", "ua": "Коди + інструкції (20 наборів)",
          "price": 59, "file": "code_instructions.txt",
          "teaser_ru": "Тизер (30%): 20 полных наборов (код + пошаговая инструкция). Полный архив — после оплаты."},
    "3": {"ru": "Удалённая работа и заработок", "en": "Remote Work & Earning", "ua": "Віддалена робота та заробіток",
          "price": 29.99, "file": "remote_earning.txt",
          "teaser_ru": "Тизер (30%): Готовые способы дистанционного заработка без вложений. Полный список с инструкциями — после оплаты."}
}

def get_text(lang, key):
    texts = {
        "start": {
            "ru": "Привет! 👋\n\nВ каждом паке есть готовые инструменты и подробная инструкция.\nТолько выберите для себя направление.\n\nВыбери язык / Choose language / Оберіть мову:",
            "en": "Hi! 👋\n\nEach pack contains ready tools and detailed instructions.\nJust choose your direction.\n\nChoose language:",
            "ua": "Привіт! 👋\n\nУ кожному пакеті є готові інструменти та детальна інструкція.\nОберіть свій напрямок.\n\nОберіть мову:"
        },
        "catalog": {
            "ru": "🛒 Магазин Grok-OMEGA — пассивный доход\n\nВыберите раздел:",
            "en": "🛒 Grok-OMEGA Store — passive income\n\nChoose section:",
            "ua": "🛒 Магазин Grok-OMEGA — пасивний дохід\n\nОберіть розділ:"
        }
    }
    return texts.get(key, {}).get(lang, texts[key]["ru"])

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"))
    markup.add(InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"))
    markup.add(InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_ua"))
    bot.reply_to(message, get_text("ru", "start"), reply_markup=markup)  # по умолчанию RU

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    lang = call.data.split('_')[1]
    current_lang[call.from_user.id] = lang
    bot.answer_callback_query(call.id)
    show_catalog(call.message)

def show_catalog(message):
    lang = current_lang.get(message.chat.id, 'ru')
    text = get_text(lang, "catalog")
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("1. Автоматизация бизнеса (20 кодов)", callback_data="buy_1"))
    markup.add(InlineKeyboardButton("2. Коды + инструкции (20 наборов)", callback_data="buy_2"))
    markup.add(InlineKeyboardButton("3. Удалённая работа и заработок", callback_data="buy_3"))
    markup.add(InlineKeyboardButton("ℹ️ О нашей компании", callback_data="about"))
    markup.add(InlineKeyboardButton("🔒 Политика конфиденциальности", callback_data="privacy"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "about")
def about_company(call):
    lang = current_lang.get(call.from_user.id, 'ru')
    text = {
        "ru": "Grok-OMEGA — команда разработчиков и предпринимателей, которая создаёт мощные инструменты автоматизации и помогает обычным людям запускать стабильный пассивный доход.\n\nС 2025 года мы сочетаем передовые технологии Grok с практическими решениями, которые уже используют сотни пользователей по всему миру.\n\nНаша цель — сделать сложные вещи простыми и доступными для каждого, кто готов сделать первый шаг.",
        "en": "Grok-OMEGA is a team of developers and entrepreneurs creating powerful automation tools and helping ordinary people launch stable passive income.\n\nSince 2025 we combine Grok technologies with practical solutions used by hundreds of users worldwide.\n\nOur goal is to make complex things simple and accessible to everyone ready to take the first step.",
        "ua": "Grok-OMEGA — команда розробників та підприємців, яка створює потужні інструменти автоматизації та допомагає звичайним людям запускати стабільний пасивний дохід.\n\nЗ 2025 року ми поєднуємо передові технології Grok з практичними рішеннями, які вже використовують сотні користувачів по всьому світу.\n\nНаша мета — зробити складні речі простими та доступними для кожного, хто готовий зробити перший крок."
    }
    bot.send_message(call.message.chat.id, text.get(lang, text["ru"]))

@bot.callback_query_handler(func=lambda call: call.data == "privacy")
def privacy_policy(call):
    text = "🔒 Политика конфиденциальности\n\nМы уважаем вашу конфиденциальность. Все данные (кошельки, контакты, платежи) используются исключительно для обработки заказов и доставки товаров.\n\nМы не передаём вашу информацию третьим лицам и не используем её в маркетинговых целях без вашего согласия.\n\nВсе платежи обрабатываются безопасно. При возникновении вопросов пишите @Volodya."
    bot.send_message(call.message.chat.id, text)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def buy_callback(call):
    num = call.data.split('_')[1]
    p = PRODUCTS[num]
    lang = current_lang.get(call.from_user.id, 'ru')
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, p['teaser_ru'] if lang == 'ru' else p.get('teaser_en', p['teaser_ru']))
    bot.send_message(call.message.chat.id, "✅ Вы выбрали: " + p[lang] if lang == 'ru' else "✅ You chose: " + p[lang])
    # Выбор оплаты
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("💎 USDT TRC20", callback_data=f"pay_usdt_{num}"))
    markup.add(InlineKeyboardButton("💳 Перевод на карту", callback_data=f"pay_card_{num}"))
    bot.send_message(call.message.chat.id, "Выберите способ оплаты:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def payment_choice(call):
    action, num = call.data.split('_')[1:]
    if action == "usdt":
        bot.send_message(call.message.chat.id, "Оплата: $" + str(PRODUCTS[num]['price']) + " USDT (TRC20)\nПереведи на:\n" + CRYPTO_WALLET + "\n\nПосле оплаты пришли TXID")
        pending_tx[call.from_user.id] = num
    else:
        bot.send_message(call.message.chat.id, "Оплата на карту:\n@Volodya\n\nПосле оплаты напиши «ОПЛАТИЛ " + num + "»")
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
                    bot.send_document(message.chat.id, f, caption="🎉 Вот твой полный товар: " + p[lang])
                bot.send_message(ADMIN_ID, "🎉 Продажа! " + p['ru'] + " за $" + str(p['price']) + " USDT")
            except:
                bot.reply_to(message, "Файл готов, но ошибка отправки. Напиши @Volodya")
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

print("🚀 Бот с 3 разделами и расширенными функциями запущен")
bot.infinity_polling()
