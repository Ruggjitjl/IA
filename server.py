from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ======= CONFIGURA TU API KEY DE DEEPSEEK ==========
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "dsta_e207917d9a5bdf8afec7de52e9d016a3809a3a6a")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"


@app.route("/")
def home():
    return "Servidor IA con DeepSeek funcionando 🚀"


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Eres un asistente útil y respondes en español."},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7
        }

        response = requests.post(DEEPSEEK_URL, headers=headers, json=payload)

        if response.status_code != 200:
            return jsonify({"error": "Error al consultar DeepSeek", "details": response.text}), 500

        result = response.json()
        ai_message = result["choices"][0]["message"]["content"]

        return jsonify({"response": ai_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Render asigna un puerto en la variable de entorno PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



