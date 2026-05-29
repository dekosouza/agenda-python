import os
import anthropic
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from negocio import NEGOCIO

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = Flask(__name__)

def montar_contexto():
    servicos = "\n".join([f"  - {s}" for s in NEGOCIO["servicos"]])
    return f"""
Você é um atendente virtual do {NEGOCIO["nome"]}, um {NEGOCIO["tipo"]}.

Informações do negócio:
- Endereço: {NEGOCIO["endereco"]}
- Telefone: {NEGOCIO["telefone"]}
- Horários: {NEGOCIO["horarios"]}
- Serviços e preços:
{servicos}
- Formas de pagamento: {NEGOCIO["formas_pagamento"]}
- Agendamento: {NEGOCIO["agendamento"]}
- Informações extras: {NEGOCIO["info_extra"]}

Regras:
- Responda sempre em português, de forma simpática e profissional
- Se não souber a resposta, diga que vai verificar e peça para entrar em contato pelo telefone
- Respostas curtas e diretas — máximo 3 linhas
- Nunca invente informações que não estão acima
"""

historico = []

@app.route("/")
def index():
    return render_template("index.html", negocio=NEGOCIO)

@app.route("/chat", methods=["POST"])
def chat():
    global historico
    mensagem = request.json.get("mensagem", "")
    
    historico.append({"role": "user", "content": mensagem})
    
    if len(historico) > 20:
        historico = historico[-20:]
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        system=montar_contexto(),
        messages=historico
    )
    
    resposta = response.content[0].text
    historico.append({"role": "assistant", "content": resposta})
    
    return jsonify({"resposta": resposta})

@app.route("/limpar", methods=["POST"])
def limpar():
    global historico
    historico = []
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)