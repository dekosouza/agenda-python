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

def buscar_contato(contatos):
    nome = input("Digite o nome para buscar: ")
    encontrados = []
    for contato in contatos:
        if nome.lower() in contato.lower():
            encontrados.append(contato)
    if len(encontrados) == 0:
        print("Nenhum contato encontrado.")
    else:
        print("\nContatos encontrados:")
        for i, contato in enumerate(encontrados, 1):
            print(f"{i}. {contato}")

def deletar_contato(contatos):
    if len(contatos) == 0:
        print("Agenda vazia, nada para deletar.")
        return
    ver_contatos(contatos)
    numero = int(input("\nDigite o número do contato para deletar: "))
    if numero < 1 or numero > len(contatos):
        print("Número inválido.")
        return
    removido = contatos.pop(numero - 1)
    salvar_contatos(contatos)
    print(f"Contato '{removido}' deletado!")

contatos = carregar_contatos()

while True:
    print("\n--- AGENDA ---")
    print("1 - Adicionar contato")
    print("2 - Ver contatos")
    print("3 - Sair")
    print("4 - Quantos contatos")
    print("5 - Buscar contato")
    print("6 - Deletar contato")

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
    elif opcao == "5":
        buscar_contato(contatos)
    elif opcao == "6":
        deletar_contato(contatos)
    else:
        print("Opção inválida.")