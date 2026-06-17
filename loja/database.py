import sqlite3
from datetime import datetime

DB = "loja.db"

def inicializar():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL NOT NULL,
            preco_original REAL,
            categoria TEXT,
            estoque INTEGER DEFAULT 0,
            imagem TEXT DEFAULT 'sem-imagem.jpg',
            destaque INTEGER DEFAULT 0,
            ativo INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            endereco TEXT NOT NULL,
            total REAL NOT NULL,
            status TEXT DEFAULT 'pendente',
            criado_em TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM produtos")
    if cursor.fetchone()[0] == 0:
        produtos_iniciais = [
            ("Camiseta Básica Branca", "100% algodão, confortável para o dia a dia", 49.90, 79.90, "Roupas", 50, "sem-imagem.jpg", 1),
            ("Calça Jeans Slim", "Jeans premium com elastano", 129.90, 199.90, "Roupas", 30, "sem-imagem.jpg", 1),
            ("Tênis Casual", "Leve e confortável para uso diário", 189.90, 249.90, "Calçados", 25, "sem-imagem.jpg", 1),
            ("Boné Ajustável", "Aba curva, regulagem traseira", 39.90, None, "Acessórios", 40, "sem-imagem.jpg", 0),
            ("Mochila Urbana", "15 litros, impermeável, porta notebook", 159.90, 219.90, "Acessórios", 20, "sem-imagem.jpg", 1),
            ("Meias Kit 6 pares", "Algodão premium, cano médio", 49.90, None, "Roupas", 100, "sem-imagem.jpg", 0),
        ]
        cursor.executemany("""
            INSERT INTO produtos (nome, descricao, preco, preco_original, categoria, estoque, imagem, destaque)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, produtos_iniciais)

    conn.commit()
    conn.close()

def listar_produtos(categoria=None, busca=None):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    query = "SELECT * FROM produtos WHERE ativo = 1"
    params = []
    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)
    if busca:
        query += " AND nome LIKE ?"
        params.append(f"%{busca}%")
    cursor.execute(query, params)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def produto_por_id(id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ? AND ativo = 1", (id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def produtos_destaque():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE destaque = 1 AND ativo = 1 LIMIT 4")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def categorias():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT categoria FROM produtos WHERE ativo = 1")
    resultado = [r[0] for r in cursor.fetchall()]
    conn.close()
    return resultado

def criar_pedido(nome, email, telefone, endereco, itens, total):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pedidos (nome, email, telefone, endereco, total, criado_em)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, email, telefone, endereco, total, datetime.now().strftime("%Y-%m-%d %H:%M")))
    pedido_id = cursor.lastrowid
    for item in itens:
        cursor.execute("""
            INSERT INTO itens_pedido (pedido_id, produto_id, nome, preco, quantidade)
            VALUES (?, ?, ?, ?, ?)
        """, (pedido_id, item["id"], item["nome"], item["preco"], item["quantidade"]))
        cursor.execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                      (item["quantidade"], item["id"]))
    conn.commit()
    conn.close()
    return pedido_id

def listar_pedidos():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos ORDER BY id DESC")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def itens_do_pedido(pedido_id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM itens_pedido WHERE pedido_id = ?", (pedido_id,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def atualizar_status_pedido(id, status):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (status, id))
    conn.commit()
    conn.close()

def listar_produtos_admin():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos ORDER BY id DESC")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def adicionar_produto(nome, descricao, preco, preco_original, categoria, estoque, destaque, imagem="sem-imagem.jpg"):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, descricao, preco, preco_original, categoria, estoque, destaque, imagem)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, descricao, float(preco),
          float(preco_original) if preco_original else None,
          categoria, int(estoque), int(destaque), imagem))
    conn.commit()
    conn.close()

def alternar_ativo(id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET ativo = CASE WHEN ativo = 1 THEN 0 ELSE 1 END WHERE id = ?", (id,))
    conn.commit()
    conn.close()