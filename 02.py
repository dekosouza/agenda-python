# Sistema de estoque de produtos
estoque = {
    "Shampoo": {"preco": 25.90, "quantidade": 50},
    "Condicionador": {"preco": 22.90, "quantidade": 30},
    "Tinta cabelo": {"preco": 45.00, "quantidade": 15},
    "Esmalte": {"preco": 8.50, "quantidade": 100},
}

def relatorio_estoque(estoque):
    print("=== RELATÓRIO DE ESTOQUE ===")
    valor_total = 0
    
    for produto, dados in estoque.items():
        valor = dados["preco"] * dados["quantidade"]
        valor_total += valor
        alerta = " ⚠️ BAIXO" if dados["quantidade"] < 20 else ""
        print(f"{produto}: {dados['quantidade']} unidades — R$ {valor:.2f}{alerta}")
    
    print(f"\nValor total em estoque: R$ {valor_total:.2f}")

def adicionar_produto(estoque, nome, preco, quantidade):
    estoque[nome] = {"preco": preco, "quantidade": quantidade}
    print(f"Produto '{nome}' adicionado!")

def atualizar_quantidade(estoque, nome, quantidade):
    if nome in estoque:
        estoque[nome]["quantidade"] += quantidade
        print(f"Estoque de '{nome}' atualizado: {estoque[nome]['quantidade']} unidades")
    else:
        print(f"Produto '{nome}' não encontrado!")

relatorio_estoque(estoque)
print()
adicionar_produto(estoque, "Hidratante", 35.00, 10)
atualizar_quantidade(estoque, "Esmalte", -5)
print()
relatorio_estoque(estoque)