import os
from flask import Flask, render_template, request, jsonify, redirect, session
from dotenv import load_dotenv
from database import inicializar, criar_agendamento, listar_agendamentos, horarios_ocupados, atualizar_status
from datetime import datetime, timedelta

load_dotenv()
app = Flask(__name__)
app.secret_key = "agendamento2024"

SENHA_ADMIN = os.getenv("SENHA_ADMIN", "admin123")

NEGOCIO = {
    "nome": "Salão da Ana",
    "tipo": "Salão de beleza",
    "cor": "#d63384",
    "whatsapp": "5513999991234",
    "servicos": [
        {"nome": "Corte feminino", "preco": "R$ 50", "duracao": 60},
        {"nome": "Corte masculino", "preco": "R$ 30", "duracao": 30},
        {"nome": "Coloração", "preco": "A partir de R$ 80", "duracao": 120},
        {"nome": "Escova", "preco": "R$ 45", "duracao": 60},
        {"nome": "Manicure", "preco": "R$ 25", "duracao": 45},
        {"nome": "Pedicure", "preco": "R$ 30", "duracao": 45},
    ],
    "horarios": ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
                 "13:00", "13:30", "14:00", "14:30", "15:00", "15:30",
                 "16:00", "16:30", "17:00", "17:30", "18:00", "18:30"]
}

inicializar()

@app.route("/")
def index():
    hoje = datetime.now()
    datas = []
    for i in range(7):
        d = hoje + timedelta(days=i+1)
        if d.weekday() != 6:
            datas.append({
                "valor": d.strftime("%Y-%m-%d"),
                "label": d.strftime("%d/%m (%A)").replace(
                    "Monday", "Segunda").replace("Tuesday", "Terça").replace(
                    "Wednesday", "Quarta").replace("Thursday", "Quinta").replace(
                    "Friday", "Sexta").replace("Saturday", "Sábado")
            })
    return render_template("index.html", negocio=NEGOCIO, datas=datas)

@app.route("/horarios-disponiveis")
def horarios_disponiveis():
    data = request.args.get("data")
    if not data:
        return jsonify([])
    ocupados = horarios_ocupados(data)
    disponiveis = [h for h in NEGOCIO["horarios"] if h not in ocupados]
    return jsonify(disponiveis)

@app.route("/agendar", methods=["POST"])
def agendar():
    dados = request.json
    id_agendamento = criar_agendamento(
        dados["nome"],
        dados["telefone"],
        dados["servico"],
        dados["data"],
        dados["horario"]
    )
    return jsonify({
        "ok": True,
        "id": id_agendamento,
        "mensagem": f"Agendamento confirmado! {dados['servico']} em {dados['data']} às {dados['horario']}."
    })

@app.route("/admin")
def admin():
    if not session.get("logado"):
        return redirect("/admin/login")
    agendamentos = listar_agendamentos()
    hoje = datetime.now().strftime("%Y-%m-%d")
    return render_template("admin.html", agendamentos=agendamentos, negocio=NEGOCIO, hoje=hoje)

@app.route("/admin/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        if request.form.get("senha") == SENHA_ADMIN:
            session["logado"] = True
            return redirect("/admin")
        erro = "Senha incorreta"
    return render_template("login.html", erro=erro, negocio=NEGOCIO)

@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/admin/login")

@app.route("/admin/status/<int:id>/<status>")
def mudar_status(id, status):
    if not session.get("logado"):
        return redirect("/admin/login")
    atualizar_status(id, status)
    return redirect("/admin")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)