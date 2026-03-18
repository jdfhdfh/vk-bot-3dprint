import os
import requests
from flask import Flask, request

app = Flask(__name__)

VK_TOKEN = os.getenv("VK_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# 🤖 ИИ (пока можно оставить простой ответ)
def ask_groq(text):
    return "Привет! 👋 Напиши, что хочешь напечатать на 3D-принтере."


# 📩 Отправка сообщения в ВК
def send_vk(user_id, message):
    requests.post("https://api.vk.com/method/messages.send", params={
        "user_id": user_id,
        "message": message,
        "random_id": 0,
        "access_token": VK_TOKEN,
        "v": "5.199"
    })


# 🏠 Проверка сервера
@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"


# 🔗 Вебхук ВК
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # 🔥 ВАЖНО — подтверждение ВК (жестко прописано)
    if data["type"] == "confirmation":
        return "c16bd2a8"

    # 💬 Новое сообщение
    if data["type"] == "message_new":
        message = data["object"]["message"]
        user_id = message["from_id"]
        text = message.get("text", "")

        if text:
            reply = ask_groq(text)
        else:
            reply = "Напиши сообщение 😊"

        send_vk(user_id, reply)

    return "ok"


# 🚀 Запуск
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
