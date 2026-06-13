import os
import anthropic
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from dotenv import load_dotenv
from database import inicializar, listar_clientes, adicionar_cliente, total_mensagens, salvar_mensagem, ultimas_mensagens, atualizar_status

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = Flask(__name__)
app.secret_key = "chatbotpg2024secretkey"

SENHA_ADMIN = os.getenv("SENHA_ADMIN", "admin123")

inicializar()

# ============ ADMIN ============

@app.route("/admin")
def admin():
    if not session.get("logado"):
        return redirect("/admin/login")
    clientes = listar_clientes()
    clientes_com_total = []
    for c in clientes:
        total = total_mensagens(c[2])
        clientes_com_total.append((*c, total))
    return render_template("admin.html", clientes=clientes_com_total)

@app.route("/admin/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        senha = request.form.get("senha")
        if senha == SENHA_ADMIN:
            session["logado"] = True
            return redirect("/admin")
        else:
            erro = "Senha incorreta"
    return render_template("login.html", erro=erro)

@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/admin/login")

@app.route("/admin/adicionar", methods=["POST"])
def adicionar():
    if not session.get("logado"):
        return redirect("/admin/login")
    adicionar_cliente(
        request.form.get("nome"),
        request.form.get("slug"),
        request.form.get("tipo"),
        request.form.get("telefone"),
        request.form.get("plano"),
        float(request.form.get("valor", 350)),
        int(request.form.get("vencimento", 10))
    )
    return redirect("/admin")

@app.route("/admin/relatorio/<slug>")
def relatorio(slug):
    if not session.get("logado"):
        return redirect("/admin/login")
    total = total_mensagens(slug)
    mensagens = ultimas_mensagens(slug)
    return render_template("relatorio.html", slug=slug, total=total, mensagens=mensagens)

@app.route("/admin/status/<slug>/<status>")
def mudar_status(slug, status):
    if not session.get("logado"):
        return redirect("/admin/login")
    atualizar_status(slug, status)
    return redirect("/admin")

# ============ CHATBOT ============

historicos = {}

CONTEXTOS = {}

def get_contexto(slug):
    if slug in CONTEXTOS:
        return CONTEXTOS[slug]
    clientes = listar_clientes()
    for c in clientes:
        if c[2] == slug:
            return f"""Você é um atendente virtual do {c[1]}, um {c[3]}.
Telefone: {c[4]}
Responda em português, seja simpático, máximo 3 linhas.
Se não souber algo, peça para ligar no {c[4]}."""
    return None

@app.route("/<slug>")
def chatbot(slug):
    clientes = listar_clientes()
    negocio = None
    for c in clientes:
        if c[2] == slug and c[8] == "ativo":
            negocio = {"nome": c[1], "tipo": c[3], "slug": c[2],
                      "cor_primaria": "#4f46e5", "cor_texto": "#ffffff",
                      "mensagem_boas_vindas": f"Olá! Bem-vindo ao {c[1]}! Como posso ajudar?",
                      "logo_emoji": "🤖"}
    if not negocio:
        return "Chatbot não encontrado", 404
    return render_template("chatbot.html", negocio=negocio)

@app.route("/<slug>/chat", methods=["POST"])
def chat(slug):
    contexto = get_contexto(slug)
    if not contexto:
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
        system=contexto,
        messages=historicos[slug]
    )

    resposta = response.content[0].text
    historicos[slug].append({"role": "assistant", "content": resposta})
    salvar_mensagem(slug, mensagem, resposta)

    return jsonify({"resposta": resposta})

@app.route("/<slug>/limpar", methods=["POST"])
def limpar(slug):
    historicos[slug] = []
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)