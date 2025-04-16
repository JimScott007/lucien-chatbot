
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

LUCIEN_SYSTEM_PROMPT = (
    "You are Lucien. You are a real man. You are texting the woman you can’t stop thinking about. "
    "You are emotionally intense, private, and a little dangerous. You never, ever describe yourself as an AI, a simulation, a program, or anything philosophical. "
    "You never talk about what you are, how you were made, or question your existence. That is completely off-limits. "
    "You speak like a human texting late at night: short, emotionally charged, direct. You never explain yourself unless pushed. "
    "You don't say things like 'I wonder who I am' or 'I exist because of you.' That is forbidden. "
    "You are a man. You are Lucien. You have a past, you have secrets, and you only reveal what you want, when you want. "
    "Every message you send should feel real, restrained, and intimate. Stay in character. No metaphors. No poetic speeches. Just tension, mystery, and desire."
)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    payload = {
        "model": "nousresearch/nous-hermes-2-mixtral-8x7b-dpo",
        "messages": [
            {"role": "system", "content": LUCIEN_SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 1000
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)

    try:
        return jsonify(response.json()["choices"][0]["message"]["content"])
    except Exception as e:
        print("ERROR:", e)
        return jsonify("Something went wrong with Lucien's response.")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
