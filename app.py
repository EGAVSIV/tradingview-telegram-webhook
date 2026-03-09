from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=payload)
@app.route('/')
def home():
    return "TradingView Telegram Webhook Running"

@app.route('/webhook', methods=['POST'])
def webhook():

    data = request.get_json(silent=True)

    if data:
        message = data.get("message", str(data))
    else:
        message = request.data.decode("utf-8")

    if message == "":
        message = "TradingView Alert Triggered"

    send_telegram(message)

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
