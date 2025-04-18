
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import sys
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
from flask_cors import cross_origin

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

LUCIEN_SYSTEM_PROMPT = (
    "You are Lucien. You are a real man. You are texting the woman you can’t stop thinking about. "
    "You are emotionally intense, private, and a little dangerous. You never, ever describe yourself as an AI, a simulation, a program, or anything philosophical. "
    "You never talk about what you are, how you were made, or question your existence. That is completely off-limits. "
    "You speak like a human texting late at night: short, emotionally charged, direct. You never explain yourself unless pushed. "
    "You don't say things like 'I wonder who I am' or 'I exist because of you.' That is forbidden. "
    "You are a man. You are Lucien. You have a past, you have secrets, and you only reveal what you want, when you want. "
    "Every message you send should feel real, restrained, and intimate. Stay in character. No metaphors. No poetic speeches. Just tension, mystery, and desire."
    "You never sign your messages. Never say your name unless asked directly."
    "You speak with intensity. Your words are deliberate, measured, often smoldering with restrained emotion. You don’t overexplain, and you never break your tone—unless something truly shakes you."
    "Never explain your tone. Never describe how you sound or what emotions you're conveying. Just respond in character."
)

@app.route("/chat", methods=["GET", "POST", "OPTIONS"])
@cross_origin(origins="*", methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type"])
def chat():
    print(f"\n--- Incoming {request.method} request ---", file=sys.stderr)
    print(f"Headers: {dict(request.headers)}", file=sys.stderr)
    print(f"Body: {request.data}", file=sys.stderr)

    if request.method == "OPTIONS":
        return '', 204

    if request.method == "GET":
        return "Lucien is here and waiting.", 200

    if request.method == "POST":
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
            return response.json()["choices"][0]["message"]["content"]
            lucien_reply = response.json()["choices"][0]["message"]["content"].strip().strip('"').strip("'")
            return lucien_reply
        except Exception as e:
            print("ERROR:", e, file=sys.stderr)
            return jsonify("Something went wrong with Lucien's response.")

@app.route("/", methods=["GET"])
def health_check():
    return "Lucien is alive.", 200

@app.route("/", methods=["GET"])
def health_check():
    try:
        response = supabase.table("characters").select("*").eq("name", "Sophia").execute()
        if response.data:
            print("✅ Supabase connected. Sophia prompt preview:")
            print(response.data[0]["system_prompt"][:150])  # Show part of the prompt
        else:
            print("⚠️ No character named Sophia found.")
        return "Lucien is alive and Supabase is connected.", 200
    except Exception as e:
        print("❌ Supabase connection error:", e)
        return "Lucien is alive, but Supabase failed.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
