import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 👉 Aquí va tu API Key de OpenRouter
API_KEY = os.getenv("OPENROUTER_API_KEY", "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")

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
            "model": "meta-llama/llama-3-8b-instruct:free",  # modelo gratis
            "messages": [{"role": "user", "content": prompt}]
        }

        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                          headers=headers, json=body)

        if r.status_code == 200:
            res = r.json()
            return jsonify({"response": res["choices"][0]["message"]["content"]})
        else:
            return jsonify({"error": "Error al consultar OpenRouter", 
                            "details": r.text}), 400
    except Exception as e:
        return jsonify({"error": "Error en el servidor", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)






