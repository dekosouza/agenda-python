import sqlite3

DB = "admin.db"

def inicializar():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL,
            telefone TEXT,
            plano TEXT DEFAULT 'Pro',
            valor REAL DEFAULT 350.0,
            vencimento INTEGER DEFAULT 10,
            status TEXT DEFAULT 'ativo',
            data_inicio TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT NOT NULL,
            mensagem TEXT NOT NULL,
            resposta TEXT NOT NULL,
            data TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def listar_clientes():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes ORDER BY status, nome")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def adicionar_cliente(nome, slug, tipo, telefone, plano, valor, vencimento):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    from datetime import datetime
    cursor.execute("""
        INSERT INTO clientes (nome, slug, tipo, telefone, plano, valor, vencimento, data_inicio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, slug, tipo, telefone, plano, valor, vencimento, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def total_mensagens(slug):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM mensagens WHERE slug = ?", (slug,))
    total = cursor.fetchone()[0]
    conn.close()
    return total

def salvar_mensagem(slug, mensagem, resposta):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    from datetime import datetime
    agora = datetime.now()
    cursor.execute("""
        INSERT INTO mensagens (slug, mensagem, resposta, data, hora)
        VALUES (?, ?, ?, ?, ?)
    """, (slug, mensagem, resposta, agora.strftime("%Y-%m-%d"), agora.strftime("%H:%M")))
    conn.commit()
    conn.close()

def ultimas_mensagens(slug, limite=10):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mensagem, resposta, data, hora FROM mensagens
        WHERE slug = ?
        ORDER BY id DESC LIMIT ?
    """, (slug, limite))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def atualizar_status(slug, status):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("UPDATE clientes SET status = ? WHERE slug = ?", (status, slug))
    conn.commit()
    conn.close()