import os
from flask import Flask, render_template, request, jsonify, redirect, session
from dotenv import load_dotenv
from database import (inicializar, listar_produtos, produto_por_id, produtos_destaque,
                      categorias, criar_pedido, listar_pedidos, itens_do_pedido,
                      atualizar_status_pedido, listar_produtos_admin, adicionar_produto, alternar_ativo)

load_dotenv()
app = Flask(__name__)
app.secret_key = "loja2024secretkey"

LOJA = {
    "nome": "Loja do Deko",
    "cor": "#2563eb",
    "whatsapp": "5513999991234",
    "descricao": "Moda e acessórios em Praia Grande"
}

SENHA_ADMIN = os.getenv("SENHA_ADMIN", "admin123")

inicializar()

# ============ LOJA ============

@app.route("/")
def index():
    destaques = produtos_destaque()
    cats = categorias()
    return render_template("index.html", loja=LOJA, destaques=destaques, categorias=cats)

@app.route("/produtos")
def produtos():
    categoria = request.args.get("categoria")
    busca = request.args.get("busca")
    lista = listar_produtos(categoria, busca)
    cats = categorias()
    return render_template("produtos.html", loja=LOJA, produtos=lista, categorias=cats,
                           categoria_ativa=categoria, busca=busca)

@app.route("/produto/<int:id>")
def produto(id):
    p = produto_por_id(id)
    if not p:
        return redirect("/produtos")
    return render_template("produto.html", loja=LOJA, produto=p)

@app.route("/carrinho")
def carrinho():
    return render_template("carrinho.html", loja=LOJA)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        dados = request.json
        pedido_id = criar_pedido(
            dados["nome"], dados["email"],
            dados["telefone"], dados["endereco"],
            dados["itens"], dados["total"]
        )
        return jsonify({"ok": True, "pedido_id": pedido_id})
    return render_template("checkout.html", loja=LOJA)

@app.route("/confirmacao/<int:id>")
def confirmacao(id):
    return render_template("confirmacao.html", loja=LOJA, pedido_id=id)

# ============ ADMIN ============

@app.route("/admin")
def admin():
    if not session.get("logado"):
        return redirect("/admin/login")
    pedidos = listar_pedidos()
    produtos = listar_produtos_admin()
    total_receita = sum(p[5] for p in pedidos if p[6] != "cancelado")
    return render_template("admin.html", loja=LOJA, pedidos=pedidos,
                           produtos=produtos, total_receita=total_receita)

@app.route("/admin/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        if request.form.get("senha") == SENHA_ADMIN:
            session["logado"] = True
            return redirect("/admin")
        erro = "Senha incorreta"
    return render_template("login.html", loja=LOJA, erro=erro)

@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/admin/login")

@app.route("/admin/pedido/<int:id>/<status>")
def mudar_status(id, status):
    if not session.get("logado"):
        return redirect("/admin/login")
    atualizar_status_pedido(id, status)
    return redirect("/admin")

@app.route("/admin/produto/adicionar", methods=["POST"])
def add_produto():
    if not session.get("logado"):
        return redirect("/admin/login")
    adicionar_produto(
        request.form.get("nome"),
        request.form.get("descricao"),
        request.form.get("preco"),
        request.form.get("preco_original") or None,
        request.form.get("categoria"),
        request.form.get("estoque"),
        request.form.get("destaque", 0)
    )
    return redirect("/admin")

@app.route("/admin/produto/toggle/<int:id>")
def toggle_produto(id):
    if not session.get("logado"):
        return redirect("/admin/login")
    alternar_ativo(id)
    return redirect("/admin")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)