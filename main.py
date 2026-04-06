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
          "teaser_ru": "20 готовых кодов, которые полностью автоматизируют продажи, сбор лидов, постинг, парсинг цен конкурентов и генерацию отчётов. Каждый код идёт с подробной инструкцией. Полная версия со всеми 20 кодами — после оплаты."},
    "2": {"ru": "Коды + подробные инструкции (20 наборов)", "en": "Codes + Instructions (20 sets)", "ua": "Коди + інструкції (20 наборів)",
          "es": "Códigos + instrucciones detalladas (20 conjuntos)", "ar": "أكواد + تعليمات مفصلة (20 مجموعة)", "fr": "Codes + instructions détaillées (20 ensembles)",
          "price": 49, "file": "code_instructions.txt",
          "teaser_ru": "20 полных наборов: готовый рабочий код + максимально подробная пошаговая инструкция на 10–15 шагов. Подходит даже полному новичку. Полная версия со всеми 20 наборами — после оплаты."},
    "3": {"ru": "Удалённая работа и заработок", "en": "Remote
