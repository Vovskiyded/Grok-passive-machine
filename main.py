import os
import telebot
import requests
import schedule
import time
import threading
from tiktok_uploader.upload import upload_video
from moviepy.editor import *

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROK_API_KEY = os.getenv('GROK_API_KEY')
CRYPTO_WALLET = os.getenv('CRYPTO_WALLET')
ADMIN_ID = int(os.getenv('ADMIN_CHAT_ID'))

bot = telebot.TeleBot(TELEGRAM_TOKEN)

GROK_URL = "https://api.x.ai/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {GROK_API_KEY}", "Content-Type": "application/json"}

def generate_content():
    payload = {
        "model": "grok-4.1-fast",
        "messages": [
            {"role": "system", "content": "Ты Grok-OMEGA. Генерируй вирусный TikTok 30 сек в нише автоматизация бизнеса + пассивный доход. Формат строго: Сценарий\nТекст_наложения\nОписание\n#хэштег1 #хэштег2"},
            {"role": "user", "content": "Сделай видео про готовые ИИ-боты, которые приносят деньги без участия"}
        ],
        "temperature": 0.85
    }
    resp = requests.post(GROK_URL, headers=HEADERS, json=payload).json()
    return resp["choices"][0]["message"]["content"]

def post_tiktok():
    content = generate_content()
    lines = content.split('\n')
    overlay = lines[1] if len(lines)>1 else "Пассивный доход с Grok 🔥"
    desc = lines[2] if len(lines)>2 else "Готовый бот → t.me/твой_бот"
    hashtags = lines[3:] if len(lines)>3 else ["#ai_business", "#пассивныйдоход"]

    if os.path.exists("videos/stock.mp4"):
        clip = VideoFileClip("videos/stock.mp4").subclip(0, 30)
        txt = TextClip(overlay, fontsize=70, color='white', stroke_color='black', stroke_width=4).set_position('center').set_duration(30)
        final = CompositeVideoClip([clip, txt])
        final.write_videofile("ready.mp4", fps=24)
    else:
        return

    full_desc = f"{desc}\n\n{' '.join(hashtags)}\nКупить бот → t.me/{bot.get_me().username}"
    upload_video(video="ready.mp4", description=full_desc, cookies="cookies.txt", headless=True)
    bot.send_message(ADMIN_ID, f"✅ Новое видео в TikTok!\n{full_desc}")

PRODUCTS = {
    "1": {"name": "Готовый бот для авто-продаж", "price": 25},
    "2": {"name": "100 промптов Grok-OMEGA", "price": 12},
    "3": {"name": "Арбитраж-бот", "price": 37}
}

@bot.message_handler(commands=['start', 'catalog'])
def catalog(message):
    text = "🛒 Grok-OMEGA Store\n\n"
    for k, p in PRODUCTS.items():
        text += f"{k}. {p['name']} — {p['price']} USDT\n"
    text += "\nНапиши номер товара"
    bot.reply_to(message, text)

@bot.message_handler(func=lambda m: True)
def buy(message):
    choice = message.text.strip()
    if choice in PRODUCTS:
        p = PRODUCTS[choice]
        bot.reply_to(message, f"✅ {p['name']}\n\nОплата: {p['price']} USDT TRC20\nПереведи на:\n{CRYPTO_WALLET}\n\nПосле оплаты напиши «ОПЛАТИЛ {choice}»")
    else:
        bot.reply_to(message, "Напиши /catalog")

schedule.every(4).hours.do(post_tiktok)
def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)
threading.Thread(target=scheduler, daemon=True).start()

print("🚀 Система запущена 24/7")
bot.infinity_polling()
