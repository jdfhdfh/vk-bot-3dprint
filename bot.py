import os
import requests
from flask import Flask, request

app = Flask(__name__)

VK_TOKEN = os.getenv("VK_TOKEN")


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
    return "ok"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    # 🔥 ПОДТВЕРЖДЕНИЕ ВК
    if data.get("type") == "confirmation":
        return "c16bd2a8", 200, {"Content-Type": "text/plain"}

    # 💬 СООБЩЕНИЕ
    if data.get("type") == "message_new":
        message = data["object"]["message"]
        user_id = message["from_id"]
        text = message.get("text", "")

        reply = "Привет! 👋 Напиши, что хочешь напечатать на 3D-принтере."
        send_vk(user_id, reply)

    return "ok", 200
