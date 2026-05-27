import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

ARQUIVO = "contatos_ia.txt"

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

Exemplos:
"adiciona João com telefone 999" → ADICIONAR: João - 999
"quem está na agenda?" → LISTAR
"tem algum Maria?" → BUSCAR: Maria
"apaga o contato 2" → DELETAR: 2
"olá" → CONVERSA: Olá! Como posso ajudar com sua agenda?
"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()

def processar_resposta(resposta, contatos):
    if resposta.startswith("ADICIONAR:"):
        dado = resposta.replace("ADICIONAR:", "").strip()
        contatos.append(dado)
        salvar_contatos(contatos)
        print(f"✓ Contato '{dado}' adicionado!")

    elif resposta.startswith("LISTAR"):
        if len(contatos) == 0:
            print("Agenda vazia.")
        else:
            print("\nSeus contatos:")
            for i, c in enumerate(contatos, 1):
                print(f"{i}. {c}")

    elif resposta.startswith("BUSCAR:"):
        nome = resposta.replace("BUSCAR:", "").strip()
        encontrados = [c for c in contatos if nome.lower() in c.lower()]
        if encontrados:
            print("\nEncontrado(s):")
            for c in encontrados:
                print(f"  - {c}")
        else:
            print("Nenhum contato encontrado.")

    elif resposta.startswith("DELETAR:"):
        num = int(resposta.replace("DELETAR:", "").strip())
        if 1 <= num <= len(contatos):
            removido = contatos.pop(num - 1)
            salvar_contatos(contatos)
            print(f"✓ Contato '{removido}' deletado!")
        else:
            print("Número inválido.")

    elif resposta.startswith("CONVERSA:"):
        mensagem = resposta.replace("CONVERSA:", "").strip()
        print(f"IA: {mensagem}")

    else:
        print(f"IA: {resposta}")

# Loop principal
contatos = carregar_contatos()
print("=== AGENDA INTELIGENTE COM CLAUDE ===")
print("Fale naturalmente! Ex: 'adiciona Maria com telefone 999'")
print("Digite 'sair' para encerrar.\n")

while True:
    comando = input("Você: ")

    if comando.lower() == "sair":
        print("Até logo!")
        break

    resposta = interpretar_comando(comando, contatos)
    processar_resposta(resposta, contatos)