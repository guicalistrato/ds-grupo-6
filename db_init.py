import sqlite3
from datetime import datetime

def init_db():
    #Inicializa o banco de dados com as tabelas necessárias. Cria tabelas: usuarios e duvidas

    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()

    # Tabela de usuários (já existe, mas deixamos para referência)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            usuario TEXT PRIMARY KEY,
            senha TEXT NOT NULL
        )
    """)

    # Tabela de dúvidas e respostas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            pergunta TEXT NOT NULL,
            resposta TEXT NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario) REFERENCES usuarios(usuario)
        )
    """)

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_db()
