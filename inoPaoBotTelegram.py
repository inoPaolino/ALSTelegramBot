import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import threading
import http.server
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
APEX_API_KEY = os.getenv("APEX_API_KEY")

latest_pred_data = "⚠️ Nessun dato ancora disponibile, riprova tra poco!"

def get_predator_cap():
    global latest_pred_data
    url = f"https://api.mozambiquehe.re/predator?auth={APEX_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        pc = data["RP"]["PC"]["val"]
        ps = data["RP"]["PS4"]["val"]
        xbox = data["RP"]["X1"]["val"]
        
        latest_pred_data = (
            f"🏆 Predator Cap:\n"
            f"💻 PC: {pc} RP\n🎮 PlayStation: {ps} RP\n🕹️ Xbox: {xbox} RP"
        )
        print("✅ Dati aggiornati dall'API")
        
    except Exception as e:
        print(f"⚠️ Errore durante la richiesta: {e}")
        
async def error_handler(update, context: ContextTypes.DEFAULT_TYPE):
    print(f"❌ Update {update} ha generato l’errore {context.error}")


async def pred(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(latest_pred_data)
    elif update.effective_chat:  # fallback: manda il messaggio al chat_id
        await context.bot.send_message(chat_id=update.effective_chat.id, text=latest_pred_data)
        
async def keep_api_alive(context: ContextTypes.DEFAULT_TYPE):
    _ = get_predator_cap()
    # non succede nulla, serve solo per tenere il traffico attivo di dati
    print("API pingata")
    
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("pred", pred))
    app.add_error_handler(error_handler)

    job_queue = app.job_queue
    job_queue.run_repeating(keep_api_alive, interval=600, first=10)
        
def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.ThreadingHTTPServer(("", port), handler)
    print(f"Keep-alive server listening on port {port}")
    httpd.serve_forever()
        
if __name__ == "__main__":
    # Avvia il bot in un thread separato
    threading.Thread(target=keep_alive, daemon=True).start()
    # Avvia il server HTTP finto
    main()









