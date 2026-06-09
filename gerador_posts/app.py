import os
import anthropic
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = Flask(__name__)

def gerar_post(tipo_negocio, tema, tom, incluir_hashtags):
    prompt = f"""Você é um especialista em marketing digital para negócios locais brasileiros.

Crie um post para Instagram para um {tipo_negocio}.

Tema do post: {tema}
Tom: {tom}
Inclui hashtags: {incluir_hashtags}

Regras:
- Escreva em português brasileiro
- Máximo 150 palavras
- Comece com uma frase impactante
- Use emojis relevantes
- Se incluir hashtags, coloque 8 a 10 no final
- Tom {tom} — adapte a linguagem

Retorne APENAS o texto do post, sem explicações."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gerar", methods=["POST"])
def gerar():
    dados = request.json
    tipo_negocio = dados.get("tipo_negocio", "")
    tema = dados.get("tema", "")
    tom = dados.get("tom", "profissional")
    incluir_hashtags = dados.get("incluir_hashtags", "sim")

    if not tipo_negocio or not tema:
        return jsonify({"erro": "Preencha todos os campos"}), 400

    post = gerar_post(tipo_negocio, tema, tom, incluir_hashtags)
    return jsonify({"post": post})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)