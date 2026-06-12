import os
import anthropic
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from database import inicializar, salvar_conversa, buscar_conversas, contar_mensagens, mensagens_por_hora
from clientes import salao_ana, restaurante_joao

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = Flask(__name__)

CLIENTES = {
    "salao-da-ana": salao_ana.NEGOCIO,
    "restaurante-do-joao": restaurante_joao.NEGOCIO,
}

historicos = {}

inicializar()

def montar_contexto(negocio):
    servicos = "\n".join([f"  - {s}" for s in negocio["servicos"]])
    return f"""
Você é um atendente virtual do {negocio["nome"]}, um {negocio["tipo"]}.
Endereço: {negocio["endereco"]}
Telefone: {negocio["telefone"]}
Horários: {negocio["horarios"]}
Serviços:
{servicos}
Pagamento: {negocio["formas_pagamento"]}
Agendamento: {negocio["agendamento"]}
Info extra: {negocio["info_extra"]}
Responda em português, seja simpático, máximo 3 linhas.
"""

@app.route("/")
def index():
    return render_template("home.html", clientes=CLIENTES.values())

@app.route("/<slug>")
def chatbot(slug):
    negocio = CLIENTES.get(slug)
    if not negocio:
        return "Cliente não encontrado", 404
    return render_template("index.html", negocio=negocio)

@app.route("/<slug>/chat", methods=["POST"])
def chat(slug):
    negocio = CLIENTES.get(slug)
    if not negocio:
        return jsonify({"erro": "não encontrado"}), 404

    if slug not in historicos:
        historicos[slug] = []

    mensagem = request.json.get("mensagem", "")
    historicos[slug].append({"role": "user", "content": mensagem})

    if len(historicos[slug]) > 20:
        historicos[slug] = historicos[slug][-20:]

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        system=montar_contexto(negocio),
        messages=historicos[slug]
    )

    resposta = response.content[0].text
    historicos[slug].append({"role": "assistant", "content": resposta})

    salvar_conversa(slug, mensagem, resposta)

    return jsonify({"resposta": resposta})

@app.route("/<slug>/limpar", methods=["POST"])
def limpar(slug):
    historicos[slug] = []
    return jsonify({"ok": True})

@app.route("/relatorio/<slug>")
def relatorio(slug):
    negocio = CLIENTES.get(slug)
    if not negocio:
        return "Cliente não encontrado", 404

    total = contar_mensagens(slug)
    conversas = buscar_conversas(slug, 10)
    horarios = mensagens_por_hora(slug)

    return render_template("relatorio.html",
        negocio=negocio,
        total=total,
        conversas=conversas,
        horarios=horarios
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)