produtos = [
    {"nome": "Corte masculino", "preco": 30},
    {"nome": "Coloração", "preco": 120},
    {"nome": "Manicure", "preco": 25},
    {"nome": "Pedicure", "preco": 30},
    {"nome": "Escova", "preco": 45},
    {"nome": "Corte feminino", "preco": 50},
    {"nome": "Hidratação", "preco": 80},
]

def analisar_precos(produtos):
    ordenados = sorted(produtos, key=lambda x: x["preco"])
    
    print("=== 3 MAIS BARATOS ===")
    for p in ordenados[:3]:
        print(f"{p['nome']} — R$ {p['preco']}")
    
    print("\n=== 3 MAIS CAROS ===")
    for p in ordenados[-3:]:
        print(f"{p['nome']} — R$ {p['preco']}")
    
media = sum(p["preco"] for p in produtos) / len(produtos)
print(f"\nMédia de preços: R$ {media:.2f}")
analisar_precos(produtos)