import sqlite3
from datetime import datetime

DB = "agendamentos.db"

def inicializar():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            servico TEXT NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            status TEXT DEFAULT 'pendente',
            criado_em TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def criar_agendamento(nome, telefone, servico, data, horario):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO agendamentos (nome, telefone, servico, data, horario, criado_em)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, telefone, servico, data, horario, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    id_novo = cursor.lastrowid
    conn.close()
    return id_novo

def listar_agendamentos():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM agendamentos
        ORDER BY data, horario
    """)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def horarios_ocupados(data):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT horario FROM agendamentos
        WHERE data = ? AND status != 'cancelado'
    """, (data,))
    resultado = [r[0] for r in cursor.fetchall()]
    conn.close()
    return resultado

def atualizar_status(id_agendamento, status):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("UPDATE agendamentos SET status = ? WHERE id = ?", (status, id_agendamento))
    conn.commit()
    conn.close()