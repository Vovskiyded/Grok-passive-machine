import os
import telebot

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CRYPTO_WALLET = os.getenv('CRYPTO_WALLET')
ADMIN_ID = int(os.getenv('ADMIN_CHAT_ID'))

bot = telebot.TeleBot(TELEGRAM_TOKEN)

PRODUCTS = {
    "1": {"name": "Готовый бот для авто-продаж", "price": 25, "file": "sales_bot.py"},
    "2": {"name": "100 промптов Grok-OMEGA", "price": 12, "file": "prompts.txt"},
    "3": {"name": "Арбитраж-бот", "price": 37, "file": "arbitrage_bot.py"}
}

# Мягкое приветствие
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

@bot.message_handler(commands=['catalog'])
def catalog(message):
    text = "🛒 Grok-OMEGA Store — деньги без участия\n\n"
    for k, p in PRODUCTS.items():
        text += f"{k}. {p['name']} — {p['price']} USDT\n"
    text += "\nНапиши номер товара"
    bot.reply_to(message, text)

@bot.message_handler(func=lambda m: True)
def handle(message):
    text = message.text.strip().upper()
    if "ОПЛАТИЛ" in text:
        try:
            num = text.split()[1]
            if num not in PRODUCTS:
                bot.reply_to(message, "Неверный номер товара")
                return
            p = PRODUCTS[num]
            bot.reply_to(message, f"✅ Оплата подтверждена!\nОтправляю твой товар...")
            try:
                with open(p['file'], "rb") as f:
                    bot.send_document(message.chat.id, f, caption=f"🎉 Вот твой товар: {p['name']}")
                bot.send_message(ADMIN_ID, f"🎉 Продажа! {p['name']} за {p['price']} USDT")
            except:
                bot.reply_to(message, "Файл готов, но ошибка отправки. Напиши @Volodya")
        except:
            bot.reply_to(message, "Напиши «ОПЛАТИЛ X», где X — номер товара")
    else:
        bot.reply_to(message, "Напиши /catalog или «ОПЛАТИЛ X»")

print("🚀 Бот с авто-доставкой и новым приветствием запущен")
bot.infinity_polling()
