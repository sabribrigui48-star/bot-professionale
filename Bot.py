import os
import requests
import json
import telebot
from telebot import types
from flask import Flask, request

# --- CONFIGURAZIONE PRIVATA ---
MY_TELEGRAM_ID = 8795594889
TELEGRAM_TOKEN = '8902053569:AAHsDt8aesAcw01xZu_qJrOk0kxQp10thB8'
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

system_instruction = (
    "Sei uno studio legale, fiscale e bancario virtuale di massimo livello, "
    "specializzato in Diritto Tedesco (DE) e Italiano (IT). "
    "Fornisci consulenze operative, tecniche, giuridiche ed economiche highly dettagliate."
)

def ask_gemini(prompt):
    if not GEMINI_API_KEY:
        return "⚠️ Errore: Chiave API Gemini non configurata nelle variabili d'ambiente di Render."
    
    # Lista di modelli da provare in ordine di priorita
    models_to_try = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.0-flash-exp"
    ]
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"{system_instruction}\n\nUtente: {prompt}"}
                ]
            }
        ]
    }
    
    last_error = ""
    
    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
            res_json = response.json()
            
            if "error" in res_json:
                last_error = res_json['error'].get('message', 'Errore sconosciuto')
                # Se il modello non e trovato, continua il ciclo e prova il successivo
                if "not found" in last_error.lower() or "not supported" in last_error.lower():
                    continue
                else:
                    return f"⚠️ Errore API Google: {last_error}"
                
            if "candidates" in res_json and len(res_json["candidates"]) > 0:
                candidate = res_json["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    return candidate["content"]["parts"][0]["text"]
        except Exception as e:
            last_error = str(e)
            continue

    return f"⚠️ Nessun modello Gemini compatibile trovato sulla tua chiave API. Dettaglio errore: {last_error}"

# Inizializzazione bot e server Flask
bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)
app = Flask(__name__)

# Configurazione automatica del Webhook su Render
WEBHOOK_URL = f"https://bot-professionale-sabri.onrender.com/{TELEGRAM_TOKEN}"
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

@app.route('/')
def home():
    return "Studio Legale & Fiscale Gemini IA - Webhook Attivo 24/7"

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    else:
        return "Forbidden", 403

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
        bot.reply_to(message, "⚙️ **Stato del Sistema**\n\n- Accesso: Blindato (ID `8795594889`)\n- Motore IA: Google Gemini Multi-Model Fallback\n- Server: Render Webhook 🟢")
        return

    wait_msg = bot.reply_to(message, "⏳ *Elaborazione dell'analisi legale/fiscale in corso...*", parse_mode="Markdown")
    ai_response = ask_gemini(user_text)
    bot.edit_message_text(ai_response, chat_id=message.chat.id, message_id=wait_msg.message_id, parse_mode="Markdown")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

