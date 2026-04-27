from functools import wraps
from flask import redirect, render_template, session, g
import sqlite3
from random import randint, seed
import time

# este arquivo foi criado para armazenar funções auxiliares

# protege paginas que precisam de login
def login_required(funcao):
    @wraps(funcao)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return funcao(*args, **kwargs)

    return decorated_function

def get_db():
    # Retorna a conexão com o banco de dados para a requisição atual.
    if 'db' not in g:
        g.db = sqlite3.connect('dados.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def salvar_duvida(usuario, pergunta, resposta, nome_chat, id_chat):
    # Salva uma dúvida e sua resposta no banco de dados.
    try:
        db = get_db()
        db.execute(
            "INSERT INTO duvidas (usuario, pergunta, resposta, nome_chat, id_chat) VALUES (?, ?, ?, ?, ?)",
            (usuario, pergunta, resposta, nome_chat, id_chat)
        )
        db.commit()
        return True
    except Exception as e:
        print(f"Erro ao salvar dúvida: {e}")
        return False

# essa função recebe as duvidas de um mesmo chat
def receber_duvidas_chat(id):
    db = get_db()
    cursor = db.execute(
        "SELECT * FROM duvidas WHERE id_chat = ?", (id,) 
    )
    resultado = cursor.fetchall()
    resultado = [dict(linha) for linha in resultado]
    return resultado

def obter_historico(usuario):
    # Obtém todas as dúvidas e respostas de um usuário, ordenadas por data decrescente.
    try:
        db = get_db()
        cursor = db.execute(
            """SELECT id, pergunta, resposta, data_criacao
               FROM duvidas
               WHERE usuario = ?
               ORDER BY data_criacao DESC""",
            (usuario,)
        )
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Erro ao obter histórico: {e}")
        return []

def obter_duvida(usuario, duvida_id):
    # Obtém uma dúvida específica de um usuário.
    try:
        db = get_db()
        cursor = db.execute(
            """SELECT id, pergunta, resposta, data_criacao
               FROM duvidas
               WHERE id = ? AND usuario = ?""",
            (duvida_id, usuario)
        )
        resultado = cursor.fetchone()
        return dict(resultado) if resultado else None
    except Exception as e:
        print(f"Erro ao obter dúvida: {e}")
        return None

# cria um id único
def criar_id():
    timeseed = int(time.time())
    seed(timeseed)

    codigo = ''
    for i in range(20):
        num = chr(randint(48, 57)) # intervalo dos numeros em ascii
        letra = chr(randint(65, 90)) # intervalo das letras maiusculas em ascii
        prob = randint(1, 2)

        # seleciona um numero ou letra aleatorio para adicionar ao codigo
        if prob == 1:
            codigo += num
        else:
            codigo += letra

    return(codigo)
