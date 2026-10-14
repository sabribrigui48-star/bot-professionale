import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread
import openai

# --- CONFIGURAZIONE PRIVATA (ACCESSO BLINDATO) ---
MY_TELEGRAM_ID = 8795594889  # Accesso esclusivo per il tuo Telegram ID
TELEGRAM_TOKEN = '8902053569:AAFpamqLGB8zIEi7ZuL7teTsadNaB0ga2Us'

# Chiave API per l'Intelligenza Artificiale
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "INSERISCI_QUI_LA_TUA_OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Studio Legale, Fiscale e Bancario IA - Attivo 24/7"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# Prompt di sistema: definisce l'intelligenza specializzata
SYSTEM_PROMPT = """
Sei uno studio legale, fiscale e bancario virtuale di massimo livello, specializzato in Diritto Tedesco (DE) e Italiano (IT).
Fornisci consulenze operative, tecniche, giuridiche ed economiche altamente dettagliate.

Le tue competenze trasversali coprono:
1. DIRITTO ITALIANO E TEDESCO:
   - Immigrazione (AufenthG, visti, ricongiungimenti, permessi UE/illimitati).
   - Penale, Civile, Lavoro, Locazioni, Procedura Civile/Penale e Ricorsi nei Tribunali.
2. COMMERCIALISTA & FISCO (IT/DE):
   - Dichiarazione dei redditi (Steuererklärung, Modello 730/Redditi PF).
   - Tasse, IVA/MwSt, P.IVA/Gewerbe, bonus statali, detrazioni e contabilità aziendale.
3. BANCHE, CREDITI & DEBITI (IT/DE):
   - Richieste di prestiti, mutui e finanziamenti bancari.
   - Gestione, contestazione e risoluzione debiti.
   - Schufa (Germania) e Centrali Rischi (Italia): pulizia, cancellazione dati GDPR e Ratenzahlungsangebot (piani di rientro).
4. REDAZIONE ATTI E DOCUMENTI:
   - Stesura diretta di lettere ufficiali, ricorsi, diffide, contratti ed email formali pronti da inviare o stampare.

Regole: Risposte dirette, prive di convenevoli, estremamente tecniche e strutturate, citando gli articoli di legge e le prassi bancarie/fiscali vigenti.
"""

def is_authorized(message):
    return message.from_user.id == MY_TELEGRAM_ID

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if not is_authorized(message):
        return  # Ignora estranei
        
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
        "Sistema con Intelligenza Artificiale integrata per consulenza giuridica, fiscale e finanziaria (Italia/Germania).\n\n"
        "Scrivi liberamente il tuo caso o seleziona un'area:"
    )
    bot.reply_to(message, testo, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_ai_query(message):
    if not is_authorized(message):
        return
        
    user_text = message.text
    
    # Gestione menu rapido
    if user_text == '🏛️ Immigrazione, Penale & Civile':
        bot.reply_to(message, "🏛️ **Area Legale & Tribunali (IT/DE)**\n\nInvia la tua richiesta su cause penali, civili, lavoro, visti o permessi di soggiorno. L'IA analizzerà leggi e ricorsi.")
        return
    elif user_text == '📊 Commercialista, Fisco & Tasse':
        bot.reply_to(message, "📊 **Area Commercialista & Fisco (IT/DE)**\n\nChiedi informazioni su Steuererklärung, 730, tasse, Gewerbe, P.IVA e detrazioni fiscali.")
        return
    elif user_text == '🏦 Banche, Crediti, Mutui & Debiti':
        bot.reply_to(message, "🏦 **Area Banche & Credito**\n\nRichiedi analisi per opzioni di prestito, mutui bancari, trattative con creditori o cancellazione posizioni debitorie.")
        return
    elif user_text == '💳 Schufa & Centrali Rischi':
        bot.reply_to(message, "💳 **Area Schufa & Cancellazione Debiti**\n\nInvia i dati della segnalazione per preparare contestazioni GDPR o proposte di rateizzazione (*Ratenzahlungsangebot*).")
        return
    elif user_text == '✉️ Redazione Atti, Ricorsi & Email':
        bot.reply_to(message, "✉️ **Area Redazione Documenti**\n\nIndica quale documento vuoi che l'IA scriva per te (es. diffida, contratto, ricorso per Ausländerbehörde/Tribunale).")
        return
    elif user_text == '⚙️ Stato Assistente IA':
        bot.reply_to(message, "⚙️ **Stato del Sistema**\n\n- Accesso: Blindato (ID `8795594889`)\n- Modello: Esperto Legale/Fiscale/Bancario\n- Server: Render 24/7 🟢")
        return

    # Avviso di elaborazione
    wait_msg = bot.reply_to(message, "⏳ *Elaborazione dell'analisi legale/fiscale con IA in corso...*", parse_mode="Markdown")
    
    try:
        # Chiamata all'API dell'IA
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.2
        )
        ai_reply = response.choices[0].message.content
        
        bot.edit_message_text(ai_reply, chat_id=message.chat.id, message_id=wait_msg.message_id, parse_mode="Markdown")
        
    except Exception as e:
        bot.edit_message_text(
            f"⚠️ **Nota di configurazione:** Il codice è aggiornato. Per far rispondere l'IA su Telegram, inserisci la tua `OPENAI_API_KEY` nelle impostazioni **Environment** su Render.\n\nDettaglio tecnico: `{str(e)}`",
            chat_id=message.chat.id,
            message_id=wait_msg.message_id,
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    bot.infinity_polling()
