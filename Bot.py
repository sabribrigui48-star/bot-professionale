import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Professionale Avanzato è attivo e operativo!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

import telebot
from telebot import types

TOKEN = '8902053569:AAE5f3x7-RXRnDd55BwJ7_qxpCJLcX2_V0w'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    btn_schufa = types.KeyboardButton('🇩🇪 Pratiche Schufa & Debiti (DE)')
    btn_legale = types.KeyboardButton('⚖️ Consulenza Legale & Contratti')
    btn_marketing = types.KeyboardButton('📈 Marketing, B2B & Vendite')
    btn_email = types.KeyboardButton('✉️ Generatore Email & Trattative')
    btn_analisi = types.KeyboardButton('📊 Analisi Aziendale & Bilanci')
    btn_impostazioni = types.KeyboardButton('⚙️ Info & Modalità d\'Uso')
    
    markup.add(btn_schufa, btn_legale, btn_marketing, btn_email, btn_analisi, btn_impostazioni)
    
    testo = (
        f"Benvenuto, {message.from_user.first_name}! 🚀\n\n"
        "Questo è il tuo **Assistente Aziendale e Legale Totale** (Italia & Germania).\n"
        "Seleziona una categoria dal menu in basso per iniziare l'operazione:"
    )
    bot.reply_to(message, testo, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    text = message.text
    
    if text == '🇩🇪 Pratiche Schufa & Debiti (DE)':
        bot.reply_to(
            message,
            "🇩🇪 **Gestione Schufa e Debiti in Germania**\n\n"
            "• Invia i dettagli o la foto del documento/sollecito ricevuto.\n"
            "• Posso redigere una proposta di rateizzazione formale (*Ratenzahlungsangebot*).\n"
            "• Posso verificare la regolarità della segnalazione secondo il GDPR e le leggi tedesche.\n\n"
            "Incolla qui i dati o descrivi la situazione."
        )
    elif text == '⚖️ Consulenza Legale & Contratti':
        bot.reply_to(
            message,
            "⚖️ **Diritto Civile e Commerciale (Italia / Germania)**\n\n"
            "• Analisi di clausole contrattuali.\n"
            "• Stesura di lettere di diffida, reclami o accordi tra aziende.\n\n"
            "Specifica il problema legale o invia il testo da esaminare."
        )
    elif text == '📈 Marketing, B2B & Vendite':
        bot.reply_to(
            message,
            "📈 **Strategie di Mercato & Lead Generation**\n\n"
            "• Analisi di prodotti, concorrenza e prezzi.\n"
            "• Creazione di piani di marketing mirati per il mercato italiano ed europeo.\n\n"
            "Dimmi cosa vendi o quale mercato vuoi aggredire."
        )
    elif text == '✉️ Generatore Email & Trattative':
        bot.reply_to(
            message,
            "✉️ **Comunicazioni e Trattative Professionali**\n\n"
            "• Scrittura di email formali a partner, avvocati e fornitori.\n"
            "• Gestione delle trattative di prezzo e accordi commerciali.\n\n"
            "Scrivi le istruzioni: es. *'Manda un'email all'avvocato X per chiudere l'accordo a queste condizioni...'*"
        )
    elif text == '📊 Analisi Aziendale & Bilanci':
        bot.reply_to(
            message,
            "📊 **Controllo di Gestione e Finanza**\n\n"
            "• Interpretazione di dati aziendali, margini di guadagno e costi.\n"
            "• Supporto per la pianificazione finanziaria.\n\n"
            "Inserisci i dati numerici o i punti chiave della tua attività."
        )
    elif text == '⚙️ Info & Modalità d\'Uso':
        bot.reply_to(
            message,
            "ℹ️ **Informazioni sul Sistema**\n\n"
            "• **Stato**: Online 24/7 su Render 🟢\n"
            "• **Modalità**: Human-in-the-loop (l'IA elabora e prepara tutto, tu dai il consenso finale prima di ogni azione).\n"
            "• **Ambiti**: Legge tedesca/italiana, commercio, marketing e automazione."
        )
    else:
        bot.reply_to(
            message,
            f"🔄 Richiesta registrata:\n\n\"{text}\"\n\n"
            "Sto elaborando l'analisi professionale basata sulle normative e strategie aziendali richieste...",
            parse_mode="Markdown"
        )

print("Bot Professionale Avanzato avviato con successo...")
bot.infinity_polling()
