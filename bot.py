import os
import requests
from flask import Flask, request

app = Flask(__name__)

VK_TOKEN = os.getenv("VK_TOKEN")
CONFIRMATION_TOKEN = os.getenv("CONFIRMATION_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def ask_groq(text):
    return "Я живой 😈"


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
    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if data["type"] == "confirmation":
        return CONFIRMATION_TOKEN

    if data["type"] == "message_new":
        user_id = data["object"]["message"]["from_id"]
        text = data["object"]["message"]["text"]

        reply = ask_groq(text)
        send_vk(user_id, reply)

    return "ok"
