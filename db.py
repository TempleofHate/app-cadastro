import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB = "clientes.db"

def conectar():
    return sqlite3.connect(DB)

def criar_tabelas():
    con = conectar()
    cur = con.cursor()
    # tabela de usuários
    cur.execute ("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,          
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    #tabela de clientes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            observacoes TEXT
            )
        """)
    con.commit()
    con.close()

def criar_usuario(username, senha_plana):
    senha_hash = generate_password_hash(senha_plana)
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO usuarios(username, password_hash) VALUES (?,?)", (username, senha_hash))
        con.commit()
        return True
    except Exception:
        return False
    finally:
        con.close()
    
def validar_usuario(username, senha_plana):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, password_hash FROM usuarios WHERE username = ?", (username,))
    linha = cur.fetchone()
    con.close()
    if linha is None:
        return None
    uid, senha_hash = linha
    if check_password_hash(senha_hash, senha_plana):
        return uid
    return None
    
#Clientes (CRUD)
def adicionar_cliente(nome, email, telefone, observacoes):
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO clientes (nome, email, telefone, observacoes) VALUES (?, ?, ?, ?)", (nome, email, telefone, observacoes))
    con.commit()
    cid = cur.lastrowid
    con.close()
    return cid

def listar_clientes():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nome, email, telefone, observacoes FROM clientes ORDER BY id")
    dados = cur.fetchall()
    con.close()
    return dados

def buscar_cliente(cid):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nome, email, telefone, observacoes FROM clientes WHERE id = ?", (cid,))
    row = cur.fetchone()
    con.close()
    return row

def atualizar_cliente(cid, nome, email, telefone, observacoes):
    con = conectar()
    cur = con.cursor()
    cur.execute("""UPDATE clientes
                SET nome = ?, email = ?, telefone = ?, observacoes = ?
                WHERE id = ?""", (nome, email, telefone, observacoes, cid))
    con.commit()
    mudou = cur.rowcount > 0
    con.close()
    return mudou

def remover_cliente(cid):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM clientes WHERE id = ?", (cid,))
    con.commit()
    apagou = cur.rowcount > 0
    con.close()
    return apagou