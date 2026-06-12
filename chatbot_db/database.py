import sqlite3
from datetime import datetime

DB = "conversas.db"

def inicializar():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            mensagem TEXT NOT NULL,
            resposta TEXT NOT NULL,
            data TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def salvar_conversa(cliente, mensagem, resposta):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    agora = datetime.now()
    cursor.execute("""
        INSERT INTO conversas (cliente, mensagem, resposta, data, hora)
        VALUES (?, ?, ?, ?, ?)
    """, (
        cliente,
        mensagem,
        resposta,
        agora.strftime("%Y-%m-%d"),
        agora.strftime("%H:%M")
    ))
    conn.commit()
    conn.close()

def buscar_conversas(cliente, limite=50):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mensagem, resposta, data, hora
        FROM conversas
        WHERE cliente = ?
        ORDER BY id DESC
        LIMIT ?
    """, (cliente, limite))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def contar_mensagens(cliente):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM conversas WHERE cliente = ?
    """, (cliente,))
    total = cursor.fetchone()[0]
    conn.close()
    return total

def mensagens_por_hora(cliente):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT substr(hora, 1, 2) as h, COUNT(*) as total
        FROM conversas
        WHERE cliente = ?
        GROUP BY h
        ORDER BY total DESC
        LIMIT 5
    """, (cliente,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado