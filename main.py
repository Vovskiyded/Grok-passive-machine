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
          "price": 49, "file": "automation_codes.txt",
          "teaser_ru": "Тизер (30%): 20 готовых кодов для автоматизации продаж, лидов, контента и рутины. Полный набор — после оплаты."},
    "2": {"ru": "Коды + подробные инструкции (20 наборов)", "en": "Codes + Instructions (20 sets)", "ua": "Коди + інструкції (20 наборів)",
          "price": 59, "file": "code_instructions.txt",
          "teaser_ru": "Тизер (30%): 20 полных наборов (код + пошаговая инструкция). Полный архив — после оплаты."},
    "3": {"ru": "Удалённая работа и заработок", "en": "Remote Work & Earning", "ua": "Віддалена робота та заробіток",
          "price": 29.99, "file": "remote_earning.txt",
          "teaser_ru": "Благодаря ИИ не обязательно быть программистом или айтишником, чтобы зарабатывать хорошие деньги.\nГлавное — решимость и желание зарабатывать.\nС остальным поможет детальная инструкция и поддержка ИИ.\n\nТизер (30%): Полный гайд по реальным способам дистанционного заработка. Пошаговые инструкции по запуску — после оплаты."}
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"))
    markup.add(InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"))
    markup.add(InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_ua"))
    bot.reply_to(message, "Привет! 👋\n\nВ каждом паке есть готовые инструменты и подробная инструкция.\nТолько выберите для себя направление.\n\nВыбери язык / Choose language / Оберіть мову:", reply_markup=markup)

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
    markup.add(InlineKeyboardButton("1. Автоматизация бизнеса (20 кодов)", callback_data="buy_1"))
    markup.add(InlineKeyboardButton("2. Коды + подробные инструкции (20 наборов)", callback_data="buy_2"))
    markup.add(InlineKeyboardButton("3. Удалённая работа и заработок", callback_data="buy_3"))
    markup.add(InlineKeyboardButton("ℹ️ О нашей компании", callback_data="about"))
    markup.add(InlineKeyboardButton("🔒 Политика конфиденциальности", callback_data="privacy"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def buy_callback(call):
    num = call.data.split('_')[1]
    p = PRODUCTS[num]
    lang = current_lang.get(call.from_user.id, 'ru')
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, p['teaser_ru'] if lang == 'ru' else p.get('teaser_en', p['teaser_ru']))
    bot.send_message(call.message.chat.id, "✅ Вы выбрали: " + p[lang] if lang == 'ru' else "✅ You chose: " + p[lang])
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
                    bot.send_document(message.chat.id, f, caption="🎉 Вот твой полный товар:")
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

print("🚀 Бот запущен с предысторией и детальными файлами")
bot.infinity_polling()
