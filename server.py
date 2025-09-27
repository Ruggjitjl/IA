import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🚀 Leer API KEY de las variables de entorno
API_KEY = os.getenv("DEEPSEEK_API_KEY")
print("API Key cargada:", API_KEY)  # 👈 línea de prueba


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }

        r = requests.post("https://api.deepseek.com/chat/completions", 
                          headers=headers, json=body)

        if r.status_code == 200:
            res = r.json()
            return jsonify({"response": res["choices"][0]["message"]["content"]})
        else:
            return jsonify({"error": "Error al consultar DeepSeek", 
                            "details": r.text}), 400
    except Exception as e:
        return jsonify({"error": "Error en el servidor", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)





