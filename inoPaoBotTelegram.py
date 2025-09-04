import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import threading
import http.server
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
APEX_API_KEY = os.getenv("APEX_API_KEY")

def get_predator_cap():
    url = f"https://api.mozambiquehe.re/predator?auth={APEX_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        pc = data["RP"]["PC"]["val"]
        ps = data["RP"]["PS4"]["val"]
        xbox = data["RP"]["X1"]["val"]

        return f"🏆 Predator Cap:\n💻 PC: {pc} RP\n🎮 PlayStation: {ps} RP\n🕹️ Xbox: {xbox} RP"

    except Exception as e:
        return f"⚠️ Errore durante la richiesta: {e}"

async def pred(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = get_predator_cap()
    await update.message.reply_text(message)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("pred", pred))
    app.run_polling()
    
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





