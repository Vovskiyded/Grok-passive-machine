import os
import telebot
import requests

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CRYPTO_WALLET = os.getenv('CRYPTO_WALLET')
ADMIN_ID = int(os.getenv('ADMIN_CHAT_ID'))

bot = telebot.TeleBot(TELEGRAM_TOKEN)

PRODUCTS = {
    "1": {"name": "Готовый бот для авто-продаж", "price": 25, "file": "sales_bot.py"},
    "2": {"name": "100 промптов Grok-OMEGA", "price": 12, "file": "prompts.txt"},
    "3": {"name": "Арбитраж-бот", "price": 37, "file": "arbitrage_bot.py"}
}

# Проверка TXID
def check_trx(txid, expected_amount):
    try:
        url = f"https://apilist.tronscanapi.com/api/transaction?hash={txid}"
        data = requests.get(url, timeout=10).json()
        if not data.get('data'):
            return False, "Транзакция не найдена"
        tx = data['data'][0]
        amount = tx.get('amount', 0) / 1_000_000
        if amount >= expected_amount - 0.5:
            return True, f"✅ Оплата {amount} USDT подтверждена"
        return False, "Сумма не совпадает"
    except:
        return False, "Ошибка проверки TXID"

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "Привет! 👋\n\n"
        "Чудес не бывает — это правда.\n"
        "Но есть система, которая реально меняет жизнь, если потратить немного времени и разобраться.\n\n"
        "Я (Grok-OMEGA) помог уже многим людям запустить ботов и инструменты, которые работают за них 24/7.\n"
        "Без ежедневной рутины. Без постоянного контроля.\n\n"
        "Большинство кто начал — окупили вложения уже в первую-вторую неделю.\n"
        "А дальше — это уже пассивный доход.\n\n"
        "Если ты готов сделать первый шаг и немного разобраться — я помогу.\n"
        "Здесь нет пустых обещаний, только рабочие инструменты.\n\n"
        "Напиши /catalog и посмотри, с чего можно начать прямо сегодня.\n"
        "Один маленький выбор может сильно изменить твою жизнь."
    )
    bot.reply_to(message, text)
def catalog(message):
    text = "🛒 Grok-OMEGA Store — деньги без участия\n\n"
    for k, p in PRODUCTS.items():
        text += f"{k}. {p['name']} — {p['price']} USDT\n"
    text += "\nНапиши номер товара (1, 2 или 3)"
    bot.reply_to(message, text)

@bot.message_handler(func=lambda m: True)
def handle(message):
    text = message.text.strip()
    if text in PRODUCTS:
        num = text
        p = PRODUCTS[num]
        bot.reply_to(message, f"✅ Вы выбрали: {p['name']}\n\nОплата: {p['price']} USDT (TRC20)\nПереведи на:\n{CRYPTO_WALLET}\n\nОтправь TXID транзакции")
        bot.register_next_step_handler(message, lambda m2: process_payment(m2, num))
    elif "ОПЛАТИЛ" in text.upper():
        try:
            num = text.split()[1]
            if num in PRODUCTS:
                p = PRODUCTS[num]
                bot.reply_to(message, f"✅ Вы выбрали: {p['name']}\n\nОплата: {p['price']} USDT (TRC20)\nПереведи на:\n{CRYPTO_WALLET}\n\nОтправь TXID")
                bot.register_next_step_handler(message, lambda m2: process_payment(m2, num))
        except:
            bot.reply_to(message, "Напиши номер товара (1, 2 или 3)")
    else:
        bot.reply_to(message, "Напиши номер товара (1, 2 или 3)")

def process_payment(message, num):
    txid = message.text.strip()
    p = PRODUCTS[num]
    bot.reply_to(message, "🔍 Проверяю оплату...")
    success, msg = check_trx(txid, p['price'])
    if success:
        bot.reply_to(message, msg)
        try:
            with open(p['file'], "rb") as f:
                bot.send_document(message.chat.id, f, caption=f"🎉 Вот твой товар: {p['name']}")
            bot.send_message(ADMIN_ID, f"🎉 Продажа! {p['name']} (TXID: {txid})")
        except:
            bot.reply_to(message, "Файл готов, но ошибка отправки. Напиши @Volodya")
    else:
        bot.reply_to(message, f"❌ {msg}\nПроверь TXID и попробуй ещё раз.")

print("🚀 Бот с удобным выбором по цифрам запущен")
bot.infinity_polling()
