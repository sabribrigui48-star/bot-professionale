
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
