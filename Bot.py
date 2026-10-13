import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot online!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

import telebot

TOKEN = '8902053569:AAHsu5l3dM87yeURIgBBKsGTx_YqmvFqVYw'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Ciao! Sono il tuo bot professionale ed sono attivo su Render!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Ho ricevuto il tuo messaggio: {message.text}")

print("Bot avviato con successo...")
bot.infinity_polling()
