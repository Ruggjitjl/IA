import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Lee tu API Key de las variables de entorno de Render
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": question}]
            }
        )
        result = response.json()

        # Extraer respuesta de la IA
        if "choices" in result:
            answer = result["choices"][0]["message"]["content"]
            return jsonify({"answer": answer})
        else:
            return jsonify({"error": result})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/")
def home():
    return "Servidor IA con DeepSeek funcionando 🚀"

