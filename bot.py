import os
import requests
from flask import Flask, request

app = Flask(__name__)

VK_TOKEN = os.getenv("VK_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
CONFIRMATION_TOKEN = os.getenv("CONFIRMATION_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def ask_groq(text):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",  # РАБОЧАЯ модель
        "messages": [
            {"role": "system", "content": "Ты дружелюбный и немного кокетливый ИИ 😈"},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except:
        print("GROQ ERROR:", response.text)
        return "Ошибка ИИ 😢"


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
