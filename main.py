from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
CHAT_ID = "6908281054"

@app.route("/")
def home():
    return "✅ Faizan™ SpyBot is Running!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        text = data["message"].get("text", "")
        chat_id = data["message"]["chat"]["id"]

        if text == "/start":
            welcome_msg = """🌟 خوش آمدید Faizan™ SpyBot میں!
یہ ایک انٹیلیجنٹ ٹریکنگ سسٹم ہے۔📡

🔗 اپنا خصوصی لنک یہاں ہے:
https://faizan-spybot.onrender.com
"""
            requests.post(f"{API_URL}/sendMessage", data={
                "chat_id": chat_id,
                "text": welcome_msg
            })

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
