from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Clave de la API de DeepSeek (guárdala como variable de entorno en Render)
API_KEY = os.getenv("e207917d9a5bdf8afec7de52e9d016a3809a3a6a")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "")

        if not question:
            return jsonify({"error": "No se recibió la pregunta"}), 400

        # Petición al modelo de DeepSeek
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": question}
            ]
        }

        r = requests.post("https://api.deepseek.com/chat/completions",
                          headers=headers, json=payload)

        if r.status_code != 200:
            return jsonify({"error": "Error al consultar DeepSeek", "details": r.text}), 500

        response_json = r.json()
        answer = response_json["choices"][0]["message"]["content"]

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
