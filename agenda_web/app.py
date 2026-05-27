import os
import anthropic
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = Flask(__name__)
ARQUIVO = "contatos.txt"

def carregar_contatos():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return f.read().splitlines()
    return []

def salvar_contatos(contatos):
    with open(ARQUIVO, "w") as f:
        for contato in contatos:
            f.write(contato + "\n")

def interpretar_comando(texto, contatos):
    lista = "\n".join(contatos) if contatos else "vazia"
    prompt = f"""
Você é um assistente de agenda de contatos.
A agenda atual tem esses contatos:
{lista}

O usuário digitou: "{texto}"

Responda APENAS com uma dessas opções:
- ADICIONAR: nome - telefone
- LISTAR
- BUSCAR: nome
- DELETAR: numero
- CONVERSA: sua resposta aqui
"""
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()

@app.route("/")
def index():
    contatos = carregar_contatos()
    return render_template("index.html", contatos=contatos)

@app.route("/comando", methods=["POST"])
def comando():
    contatos = carregar_contatos()
    texto = request.json.get("texto", "")
    resposta = interpretar_comando(texto, contatos)

    mensagem = ""

    if resposta.startswith("ADICIONAR:"):
        dado = resposta.replace("ADICIONAR:", "").strip()
        contatos.append(dado)
        salvar_contatos(contatos)
        mensagem = f"✓ Contato '{dado}' adicionado!"

    elif resposta.startswith("LISTAR"):
        mensagem = "Mostrando todos os contatos."

    elif resposta.startswith("BUSCAR:"):
        nome = resposta.replace("BUSCAR:", "").strip()
        encontrados = [c for c in contatos if nome.lower() in c.lower()]
        mensagem = f"Encontrado(s): {', '.join(encontrados)}" if encontrados else "Nenhum contato encontrado."

    elif resposta.startswith("DELETAR:"):
        num = int(resposta.replace("DELETAR:", "").strip())
        if 1 <= num <= len(contatos):
            removido = contatos.pop(num - 1)
            salvar_contatos(contatos)
            mensagem = f"✓ Contato '{removido}' deletado!"
        else:
            mensagem = "Número inválido."

    elif resposta.startswith("CONVERSA:"):
        mensagem = resposta.replace("CONVERSA:", "").strip()

    else:
        mensagem = resposta

    contatos = carregar_contatos()
    return jsonify({"mensagem": mensagem, "contatos": contatos})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)