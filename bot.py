import os
import requests
from flask import Flask, request

app = Flask(__name__)

VK_TOKEN = os.environ.get("VK_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
CONFIRMATION_TOKEN = os.environ.get("CONFIRMATION_TOKEN")


def send_message(user_id, message):
    requests.post("https://api.vk.com/method/messages.send", data={
        "user_id": user_id,
        "message": message,
        "random_id": 0,
        "access_token": VK_TOKEN,
        "v": "5.131"
    })


def ask_groq(user_message):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": """Ты помощник мастерской 3D печати в Ессентуках. Тебя зовут Печатник.
Ты помогаешь клиентам: отвечаешь на вопросы о 3D печати, принимаешь заказы, рассказываешь о возможностях.
Что мы печатаем: фигурки, сувениры, украшения, аксессуары, запчасти, детали — любые изделия под заказ.
Материалы: PLA, PETG, ABS и другие пластики.
Сроки: обычно 1-3 дня.
Для заказа нужно: описание изделия или файл STL, размеры, материал.
Цены: рассчитываются индивидуально.
Отвечай коротко, дружелюбно и по делу."""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )

        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            print("GROQ ERROR:", result)
            return "Ошибка ответа от ИИ"

    except Exception as e:
        print("EXCEPTION:", e)
        return "Извините, произошла ошибка. Напишите нам напрямую!"


@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if data.get("type") == "confirmation":
        return CONFIRMATION_TOKEN

    if data.get("type") == "message_new":
        message = data["object"]["message"]
        user_id = message["from_id"]
        text = message["text"]

        reply = ask_groq(text)
        send_message(user_id, reply)

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
