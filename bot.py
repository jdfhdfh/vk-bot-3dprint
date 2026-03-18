import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VK_TOKEN = os.getenv("VK_TOKEN")
CONFIRMATION_TOKEN = os.getenv("CONFIRMATION_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# 🔥 Запрос к GROQ (реальный ИИ)
def ask_groq(text):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": "Ты помощник сервиса 3D печати. Отвечай кратко, дружелюбно и продающе."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print("GROQ ERROR:", e)
        return "Ошибка ИИ 😢 Попробуй позже."


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

    if not data:
        return "no data"

    # 🔐 Подтверждение сервера ВК
    if data["type"] == "confirmation":
        return CONFIRMATION_TOKEN

    # 💬 Новое сообщение
    if data["type"] == "message_new":
        message = data["object"]["message"]
        user_id = message["from_id"]
        text = message.get("text", "")

        if text:
            reply = ask_groq(text)
        else:
            reply = "Напиши текст 😊"

        send_vk(user_id, reply)

    return "ok"


# 🚀 Запуск для Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
