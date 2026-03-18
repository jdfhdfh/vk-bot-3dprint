import os
import requests
from flask import Flask, request

app = Flask(__name__)

VK_TOKEN = os.getenv("VK_TOKEN")


def ask_groq(text):
    return "Привет! 👋 Напиши, что хочешь напечатать на 3D-принтере."


def send_vk(user_id, message):
    requests.post("https://api.vk.com/method/messages.send", params={
        "user_id": user_id,
        "message": message,
        "random_id": 0,
        "access_token": VK_TOKEN,
        "v": "5.199"
    })


@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if not data:
        return "no data"

    # ✅ подтверждение ВК
    if data.get("type") == "confirmation":
        return "c16bd2a8"

    # 💬 сообщения
    if data.get("type") == "message_new":
        message = data["object"]["message"]
        user_id = message["from_id"]
        text = message.get("text", "")

        if text:
            reply = ask_groq(text)
        else:
            reply = "Напиши сообщение 😊"

        send_vk(user_id, reply)

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
