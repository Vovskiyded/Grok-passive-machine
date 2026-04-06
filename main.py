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
          "price": 49, "file": "automation_codes.txt",
          "teaser_ru": "20 готовых кодов для автоматизации продаж, лидов, контента и рутины. Каждый код идёт с подробной инструкцией. Полная версия — после оплаты."},
    "2": {"ru": "Коды + подробные инструкции (20 наборов)", "en": "Codes + Instructions (20 sets)", "ua": "Коди + інструкції (20 наборів)",
          "es": "Códigos + instrucciones detalladas (20 conjuntos)", "ar": "أكواد + تعليمات مفصلة (20 مجموعة)", "fr": "Codes + instructions détaillées (20 ensembles)",
          "price": 59, "file": "code_instructions.txt",
          "teaser_ru": "20 полных наборов (код + пошаговая инструкция на 10–15 шагов). Идеально даже для полного новичка. Полная версия — после оплаты."},
    "3": {"ru": "Удалённая работа и заработок", "en": "Remote Work & Earning", "ua": "Віддалена робота та заробіток",
          "es": "Trabajo remoto y ganancias", "ar": "العمل عن بعد والكسب", "fr": "Travail à distance et revenus",
          "price": 29.99, "file": "remote_earning.txt",
          "teaser_ru": "Благодаря ИИ не обязательно быть программистом или айтишником, чтобы зарабатывать хорошие деньги. Главное — решимость и желание зарабатывать. С остальным поможет детальная инструкция и поддержка ИИ. Полная версия — после оплаты."}
}

def get_text(lang, key):
    texts = {
        "start": {
            "ru": "Привет! 👋\n\nВ каждом паке есть готовые инструменты и подробная инструкция.\nТолько выберите для себя направление.\n\nВыбери язык:",
            "en": "Hi! 👋\n\nEach pack has ready tools and detailed instructions.\nJust choose your direction.\n\nChoose language:",
            "ua": "Привіт! 👋\n\nУ кожному пакеті є готові інструменти та детальна інструкція.\nОберіть свій напрямок.\n\nОберіть мову:",
            "es": "¡Hola! 👋\n\nCada paquete tiene herramientas listas e instrucciones detalladas.\nSolo elige tu dirección.\n\nElige idioma:",
            "ar": "مرحبا! 👋\n\nكل حزمة تحتوي على أدوات جاهزة وتعليمات مفصلة.\nاختر اتجاهك فقط.\n\nاختر اللغة:",
            "fr": "Bonjour ! 👋\n\nChaque pack contient des outils prêts et des instructions détaillées.\nChoisissez simplement votre direction.\n\nChoisissez la langue:"
        },
        "catalog": {
            "ru": "🛒 Магазин Grok-OMEGA — пассивный доход\n\nВыберите раздел:",
            "en": "🛒 Grok-OMEGA Store — passive income\n\nChoose section:",
            "ua": "🛒 Магазин Grok-OMEGA — пасивний дохід\n\nОберіть розділ:",
            "es": "🛒 Tienda Grok-OMEGA — ingresos pasivos\n\nElige sección:",
            "ar": "🛒 متجر Grok-OMEGA — دخل سلبي\n\nاختر القسم:",
            "fr": "🛒 Boutique Grok-OMEGA — revenus passifs\n\nChoisissez la section:"
        }
    }
    return texts.get(key, {}).get(lang, texts[key]["ru"])

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("Русский", callback_data="lang_ru"))
    markup.add(InlineKeyboardButton("English", callback_data="lang_en"))
    markup.add(InlineKeyboardButton("Українська", callback_data="lang_ua"))
    markup.add(InlineKeyboardButton("Español", callback_data="lang_es"))
    markup.add(InlineKeyboardButton("العربية", callback_data="lang_ar"))
    markup.add(InlineKeyboardButton("Français", callback_data="lang_fr"))
    bot.reply_to(message, get_text("ru", "start"), reply_markup=markup)

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
    markup.add(InlineKeyboardButton("2. Коды + подробные инструкции (20 наборов)", callback_data="buy_2"))
    markup.add(InlineKeyboardButton("3. Удалённая работа и заработок", callback_data="buy_3"))
    markup.add(InlineKeyboardButton("ℹ️ О нашей компании", callback_data="about"))
    markup.add(InlineKeyboardButton("🔒 Политика конфиденциальности", callback_data="privacy"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "about")
def about_company(call):
    lang = current_lang.get(call.from_user.id, 'ru')
    text = {
        "ru": "Grok-OMEGA — это команда разработчиков и предпринимателей, которая создаёт мощные инструменты автоматизации бизнеса. С 2025 года мы помогаем обычным людям запускать стабильный пассивный доход без специального образования. Мы сочетаем передовые возможности ИИ с практическими решениями, которые уже используют сотни пользователей по всему миру. Наша цель — сделать сложные вещи простыми и доступными для каждого, кто готов сделать первый шаг.",
        "en": "Grok-OMEGA is a team of developers and entrepreneurs creating powerful business automation tools. Since 2025 we help ordinary people launch stable passive income without special education. We combine advanced AI capabilities with practical solutions already used by hundreds of users worldwide. Our goal is to make complex things simple and accessible to everyone ready to take the first step.",
        "ua": "Grok-OMEGA — це команда розробників та підприємців, яка створює потужні інструменти автоматизації бізнесу. З 2025 року ми допомагаємо звичайним людям запускати стабільний пасивний дохід без спеціальної освіти. Ми поєднуємо передові можливості ІІ з практичними рішеннями, які вже використовують сотні користувачів по всьому світу. Наша мета — зробити складні речі простими та доступними для кожного, хто готовий зробити перший крок.",
        "es": "Grok-OMEGA es un equipo de desarrolladores y empresarios que crean herramientas poderosas de automatización de negocios. Desde 2025 ayudamos a personas comunes a lanzar ingresos pasivos estables sin educación especial.",
        "ar": "Grok-OMEGA هو فريق من المطورين ورجال الأعمال الذين يصنعون أدوات أتمتة أعمال قوية. منذ 2025 نساعد الأشخاص العاديين على إطلاق دخل سلبي مستقر بدون تعليم خاص.",
        "fr": "Grok-OMEGA est une équipe de développeurs et d'entrepreneurs qui créent des outils puissants d'automatisation des entreprises. Depuis 2025, nous aidons les gens ordinaires à lancer des revenus passifs stables sans éducation spéciale."
    }
    bot.send_message(call.message.chat.id, text.get(lang, text["ru"]))

@bot.callback_query_handler(func=lambda call: call.data == "privacy")
def privacy_policy(call):
    text = "🔒 Политика конфиденциальности\n\nМы уважаем вашу конфиденциальность и защищаем ваши данные.\nВсе данные (токены, кошельки, платежи, переписка) используются исключительно для обработки заказов и доставки товаров.\nМы не передаём вашу информацию третьим лицам, не используем её в маркетинге и не продаём.\nВсе платежи обрабатываются безопасно. При возникновении любых вопросов пишите @grom_ii."
    bot.send_message(call.message.chat.id, text)

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

print("🚀 Бот запущен с новыми языками, расширенными текстами и @grom_ii")
bot.infinity_polling()
