
import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread
import google.generativeai as genai

# --- CONFIGURAZIONE PRIVATA ---
MY_TELEGRAM_ID = 8795594889
TELEGRAM_TOKEN = '8902053569:AAFpamqLGB8zIEi7ZuL7teTsadNaB0ga2Us'

# Chiave API Gemini letta dalle variabili d'ambiente di Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

system_instruction = """
Sei uno studio legale, fiscale e bancario virtuale di massimo livello, specializzato in Diritto Tedesco (DE) e Italiano (IT).
Fornisci consulenze operative, tecniche, giuridiche ed economiche altamente dettagliate.

Le tue competenze coprono:
1. DIRITTO ITALIANO E TEDESCO (Immigrazione, Penale, Civile, Lavoro, Locazioni).
2. COMMERCIALISTA & FISCO (Steuererklärung, 730, MwSt/IVA, Gewerbe, P.IVA).
3. BANCHE, CREDITI & DEBITI (Prestiti, Mutui, Trattative con creditori).
4. SCHUFA & CENTRALI RISCHI (Cancellazione dati GDPR, Ratenzahlungsangebot).
5. REDAZIONE ATTI (Ricorsi, diffide, contratti, email formali).

Risposte dirette, prive di convenevoli, estremamente tecniche e strutturate con riferimenti normativi.
"""

# Configurazione modello Gemini
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )
except Exception:
    model = None

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Studio Legale & Fiscale Gemini IA - Server Attivo 24/7"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

keep_alive()

def is_authorized(message):
    return message.from_user.id == MY_TELEGRAM_ID

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if not is_authorized(message):
        return
        
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    btn_1 = types.KeyboardButton('🏛️ Immigrazione, Penale & Civile')
    btn_2 = types.KeyboardButton('📊 Commercialista, Fisco & Tasse')
    btn_3 = types.KeyboardButton('🏦 Banche, Crediti, Mutui & Debiti')
    btn_4 = types.KeyboardButton('💳 Schufa & Centrali Rischi')
    btn_5 = types.KeyboardButton('✉️ Redazione Atti, Ricorsi & Email')
    btn_6 = types.KeyboardButton('⚙️ Stato Assistente IA')
    
    markup.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6)
    
    testo = (
        f"🔒 **Studio Legale, Fiscale e Bancario Privato di {message.from_user.first_name}**\n\n"
        "Sistema con Intelligenza Artificiale Google Gemini per consulenza giuridica, fiscale e finanziaria (Italia/Germania).\n\n"
        "Scrivi liberamente il tuo caso o seleziona un'area:"
    )
    bot.reply_to(message, testo, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_ai_query(message):
    if not is_authorized(message):
        return
        
    user_text = message.text
    
    if user_text == '🏛️ Immigrazione, Penale & Civile':
        bot.reply_to(message, "🏛️ **Area Legale & Tribunali (IT/DE)**\n\nInvia la tua richiesta su cause penali, civili, lavoro, visti o permessi di soggiorno.")
        return
    elif user_text == '📊 Commercialista, Fisco & Tasse':
        bot.reply_to(message, "📊 **Area Commercialista & Fisco (IT/DE)**\n\nChiedi informazioni su Steuererklärung, 730, tasse, Gewerbe, P.IVA e detrazioni.")
        return
    elif user_text == '🏦 Banche, Crediti, Mutui & Debiti':
        bot.reply_to(message, "🏦 **Area Banche & Credito**\n\nRichiedi analisi per prestiti, mutui bancari, trattative con creditori o cancellazione debiti.")
        return
    elif user_text == '💳 Schufa & Centrali Rischi':
        bot.reply_to(message, "💳 **Area Schufa & Cancellazione Debiti**\n\nInvia i dati della segnalazione per preparare contestazioni GDPR o proposte di rateizzazione.")
        return
    elif user_text == '✉️ Redazione Atti, Ricorsi & Email':
        bot.reply_to(message, "✉️ **Area Redazione Documenti**\n\nIndica quale documento vuoi che l'IA scriva per te (diffida, contratto, ricorso).")
        return
    elif user_text == '⚙️ Stato Assistente IA':
        bot.reply_to(message, "⚙️ **Stato del Sistema**\n\n- Accesso: Blindato (ID `8795594889`)\n- Motore IA: Google Gemini Flash\n- Server: Render 24/7 🟢")
        return

    wait_msg = bot.reply_to(message, "⏳ *Elaborazione dell'analisi legale/fiscale in corso...*", parse_mode="Markdown")
    
    try:
        if not model:
            bot.edit_message_text("⚠️ **Errore:** Modello Gemini non inizializzato. Controlla `GEMINI_API_KEY` su Render.", chat_id=message.chat.id, message_id=wait_msg.message_id)
            return

        response = model.generate_content(user_text)
        bot.edit_message_text(response.text, chat_id=message.chat.id, message_id=wait_msg.message_id, parse_mode="Markdown")
        
    except Exception as e:
        bot.edit_message_text(
            f"⚠️ **Errore di risposta IA:** `{str(e)}`\n\nVerifica la chiave `GEMINI_API_KEY` nelle impostazioni Environment su Render.",
            chat_id=message.chat.id,
            message_id=wait_msg.message_id,
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    bot.infinity_polling(skip_pending_updates=True)
