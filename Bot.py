import os
from flask import Flask
from threading import Thread
import telebot
from telebot import types

# --- CONFIGURAZIONE PRIVATA (ACCESSO BLINDATO) ---
MY_TELEGRAM_ID = 8795594889  # Il tuo ID Telegram personale

TOKEN = '8902053569:AAFpamqLGB8zIEi7ZuL7teTsadNaB0ga2Us'
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Assistente Privato - Riservato"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# Controllo di sicurezza: autorizza SOLO te
def is_authorized(message):
    return message.from_user.id == MY_TELEGRAM_ID

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if not is_authorized(message):
        return  # Ignora totalmente chiunque altro
        
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    btn_schufa = types.KeyboardButton('🇩🇪 Pratiche Schufa & Debiti (DE)')
    btn_legale = types.KeyboardButton('⚖️ Consulenza Legale & Contratti')
    btn_marketing = types.KeyboardButton('📈 Marketing, B2B & Vendite')
    btn_email = types.KeyboardButton('✉️ Generatore Email & Trattative')
    btn_analisi = types.KeyboardButton('📊 Analisi Aziendale & Bilanci')
    btn_impostazioni = types.KeyboardButton('⚙️ Info & Modalità D\'Uso')
    
    markup.add(btn_schufa, btn_legale, btn_marketing, btn_email, btn_analisi, btn_impostazioni)
    
    testo = (
        f"🔒 **Archivio & Assistente Privato di {message.from_user.first_name}**\n\n"
        "Sistema ad uso personale esclusivo per ricerche legali, analisi documenti e gestione pratiche riservate.\n\n"
        "Seleziona una sezione dal menu per iniziare:"
    )
    bot.reply_to(message, testo, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    if not is_authorized(message):
        return  # Ignora estranei
        
    text = message.text
    
    if text == '🇩🇪 Pratiche Schufa & Debiti (DE)':
        bot.reply_to(
            message,
            "🇩🇪 **Gestione Schufa e Debiti in Germania**\n\n"
            "- Invia i dettagli o la foto del documento/sollecito ricevuto.\n"
            "- Redazione di proposte di rateizzazione formali (*Ratenzahlungsangebot*).\n"
            "- Verifiche di regolarità della segnalazione (GDPR e norme tedesche).\n\n"
            "Incolla qui i dati o il documento da esaminare."
        )
    elif text == '⚖️ Consulenza Legale & Contratti':
        bot.reply_to(
            message,
            "⚖️ **Diritto Civile e Commerciale (Italia / Germania)**\n\n"
            "- Analisi di clausole contrattuali.\n"
            "- Stesura di lettere di diffida, reclami o bozze di accordi.\n\n"
            "Inserisci il testo o l'argomento legale da esaminare."
        )
    elif text == '📈 Marketing, B2B & Vendite':
        bot.reply_to(
            message,
            "📈 **Strategie & Ricerche di Mercato**\n\n"
            "- Analisi di prodotti, concorrenza e prezzi.\n"
            "- Piani strategici per mercati italiano ed europeo."
        )
    elif text == '✉️ Generatore Email & Trattative':
        bot.reply_to(
            message,
            "✉️ **Comunicazioni e Trattative Riservate**\n\n"
            "- Scrittura email formali per partner, legali e fornitori.\n"
            "- Gestione trattative e condizioni commerciali."
        )
    elif text == '📊 Analisi Aziendale & Bilanci':
        bot.reply_to(
            message,
            "📊 **Controllo di Gestione Privato**\n\n"
            "- Calcolo margini, costi e pianificazione finanziaria.\n"
            "Inserisci i dati o i calcoli numerici da elaborare."
        )
    elif text == '⚙️ Info & Modalità D\'Uso':
        bot.reply_to(
            message,
            "⚙️ **Stato del Sistema**\n\n"
            "- **Modalità:** Privata ed esclusiva (ID protetto) 🔒\n"
            "- **Stato:** Attivo e operativo su Render 🟢"
        )
    else:
        bot.reply_to(
            message,
            f"📥 **Dati e note ricevute:**\n\n\"{text}\"\n\n"
            "Sto elaborando l'analisi privata e la preparazione dei documenti richiesti...",
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    bot.infinity_polling()
