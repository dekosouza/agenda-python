import os

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

def adicionar_contato(contatos):
    nome = input("Nome do contato: ")
    telefone = input("Telefone: ")
    contatos.append(f"{nome} - {telefone}")
    salvar_contatos(contatos)
    print(f"Contato {nome} adicionado e salvo!")

def ver_contatos(contatos):
    if len(contatos) == 0:
        print("Agenda vazia.")
    else:
        print("\nSeus contatos:")
        for i, contato in enumerate(contatos, 1):
            print(f"{i}. {contato}")

def contar_contatos(contatos):
    print(f"Você tem {len(contatos)} contato(s).")

contatos = carregar_contatos()

while True:
    print("\n--- AGENDA ---")
    print("1 - Adicionar contato")
    print("2 - Ver contatos")
    print("3 - Sair")
    print("4 - Quantos contatos")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        adicionar_contato(contatos)
    elif opcao == "2":
        ver_contatos(contatos)
    elif opcao == "3":
        print("Saindo... até logo!")
        break
    elif opcao == "4":
        contar_contatos(contatos)
    else:
        print("Opção inválida.")