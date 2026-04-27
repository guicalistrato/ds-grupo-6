import pytest
import sqlite3
from unittest.mock import patch
from app import app

# ============= CONFIGURAÇÃO =============

@pytest.fixture
def client():
    """Configura a aplicação para testes com banco em memória."""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"

    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.executescript("""
        CREATE TABLE usuarios (
            usuario TEXT PRIMARY KEY,
            senha TEXT NOT NULL
        );
        CREATE TABLE duvidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            pergunta TEXT NOT NULL,
            resposta TEXT NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario) REFERENCES usuarios(usuario)
        );
    """)

    with patch('app.get_db', return_value=db):
        with app.test_client() as client:
            yield client

@pytest.fixture
def client_logado(client):
    """Cria uma conta e loga, retorna o client já autenticado."""
    client.post('/criar-conta', json={
        "usuario": "teste",
        "senha": "senha123",
        "senha_confirma": "senha123"
    })
    client.post('/login', json={
        "usuario": "teste",
        "senha": "senha123"
    })
    return client

# ============= TESTES: CRIAR CONTA =============

def test_criar_conta_sucesso(client):
    res = client.post('/criar-conta', json={
        "usuario": "novo",
        "senha": "senha123",
        "senha_confirma": "senha123"
    })
    assert res.status_code == 200
    assert res.get_json()["redirect"] == "/login"

def test_criar_conta_usuario_duplicado(client):
    client.post('/criar-conta', json={
        "usuario": "duplicado",
        "senha": "senha123",
        "senha_confirma": "senha123"
    })
    res = client.post('/criar-conta', json={
        "usuario": "duplicado",
        "senha": "senha123",
        "senha_confirma": "senha123"
    })
    assert res.status_code == 400
    assert "erro" in res.get_json()

def test_criar_conta_senhas_diferentes(client):
    res = client.post('/criar-conta', json={
        "usuario": "alguem",
        "senha": "abc",
        "senha_confirma": "xyz"
    })
    assert res.status_code == 400

def test_criar_conta_campos_vazios(client):
    res = client.post('/criar-conta', json={
        "usuario": "",
        "senha": "",
        "senha_confirma": ""
    })
    assert res.status_code == 400

# ============= TESTES: LOGIN =============

def test_login_sucesso(client):
    client.post('/criar-conta', json={
        "usuario": "teste",
        "senha": "senha123",
        "senha_confirma": "senha123"
    })
    res = client.post('/login', json={
        "usuario": "teste",
        "senha": "senha123"
    })
    assert res.status_code == 200
    assert res.get_json()["redirect"] == "/"

def test_login_senha_errada(client):
    client.post('/criar-conta', json={
        "usuario": "teste",
        "senha": "senha123",
        "senha_confirma": "senha123"
    })
    res = client.post('/login', json={
        "usuario": "teste",
        "senha": "errada"
    })
    assert res.status_code == 401

def test_login_usuario_inexistente(client):
    res = client.post('/login', json={
        "usuario": "naoexiste",
        "senha": "qualquer"
    })
    assert res.status_code == 401

# ============= TESTES: HISTÓRICO =============

def test_historico_sem_autenticacao(client):
    res = client.get('/historico')
    assert res.status_code == 401

def test_historico_usuario_anonimo(client):
    client.post('/continuar-sem-login')
    res = client.get('/historico')
    assert res.status_code == 401

def test_historico_usuario_logado(client_logado):
    res = client_logado.get('/historico')
    assert res.status_code == 200
    assert "duvidas" in res.get_json()

def test_historico_duvida_inexistente(client_logado):
    res = client_logado.get('/historico/99999')
    assert res.status_code == 404

# ============= TESTES: SESSÃO ANÔNIMA =============

def test_continuar_sem_login(client):
    res = client.post('/continuar-sem-login')
    assert res.status_code == 200
    assert res.get_json()["redirect"] == "/"

def test_anonimo_nao_acessa_historico(client):
    client.post('/continuar-sem-login')
    res = client.get('/historico')
    assert res.status_code == 401