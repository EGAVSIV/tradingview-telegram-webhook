from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Read secrets from Render Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Telegram sending function
def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": msg
        }

        r = requests.post(url, data=payload)
        print("Telegram response:", r.text)

    except Exception as e:
        print("Telegram Error:", e)


# Home route (for testing)
@app.route('/')
def home():
    return "TradingView Telegram Webhook Running"


# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():

    try:
        data = request.get_json(silent=True)

        # If JSON alert
        if data:
            message = data.get("message", str(data))
        else:
            message = request.data.decode("utf-8")

        if not message:
            message = "TradingView Alert Triggered"

        print("Incoming Alert:", message)

        send_telegram(message)

        return {"status": "success"}, 200

    except Exception as e:
        print("Webhook Error:", e)
        return {"status": "error"}, 500


# Run server (Render uses Gunicorn but keep for safety)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
