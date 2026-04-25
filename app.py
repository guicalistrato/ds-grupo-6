from flask import Flask, render_template, redirect, request, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import sqlite3
from boole import run_boole

from funcoes import login_required, get_db, salvar_duvida, obter_duvida, obter_historico, criar_id

# configuração inicial
app = Flask(__name__)

# armazena os dados no servidor ao invés dos cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# garante que usuário não consiga acessar versões antigas
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# ============= BANCO DE DADOS =============
@app.teardown_appcontext
def close_db(e=None):
    # Fecha a conexão com o banco de dados ao fim de cada requisição.
    db = g.pop('db', None)
    if db is not None:
        db.close()

# ============= ROTAS =============
# página inicial
@app.get("/")
@login_required
def index_get():
    return render_template("index.html")

@app.post("/")
@login_required
def index_post():
    dados = request.get_json()
    if not dados:
        return {"erro": "Dados não recebidos"}, 400

    duvida = dados.get('duvida', '').strip()
    if not duvida:
        return {"erro": "Dúvida não pode estar vazia"}, 400

    resultados = run_boole(duvida)
    resposta_boole = resultados[0]
    titulo = resultados[1] 
    print(titulo)

    # cria um id pro chat
    id_chat = criar_id()

    usuario = session.get("user_id")
    salvar_duvida(usuario, duvida, resposta_boole, titulo, id_chat)

    return {"resultado": resposta_boole, "titulo": titulo}, 200

# rota para obter histórico de dúvidas
@app.get("/historico")
@login_required
def obter_historico_route():
    usuario = session.get("user_id")
    historico = obter_historico(usuario)
    return {"duvidas": historico}, 200

# rota para obter uma dúvida específica
@app.get("/historico/<int:duvida_id>")
@login_required
def obter_duvida_route(duvida_id):
    usuario = session.get("user_id")
    duvida = obter_duvida(usuario, duvida_id)

    if not duvida:
        return {"erro": "Dúvida não encontrada"}, 404

    return duvida, 200

# página de login
@app.get('/login')
def login_get():
    if session.get("user_id"):
        return redirect("/")
    return render_template('login.html')

@app.post('/login')
def login_post():
    session.clear()
    dados = request.get_json()

    if not dados:
        return {"erro": "Dados não recebidos"}, 400

    usuario = dados.get('usuario')
    senha = dados.get('senha')

    if not usuario or not senha:
        return {"erro": "Usuário e senha são obrigatórios"}, 400

    db = get_db()
    row = db.execute(
        "SELECT senha FROM usuarios WHERE usuario = ?", (usuario,)
    ).fetchone()

    if row and check_password_hash(row["senha"], senha):
        session["user_id"] = usuario
        return {"redirect": "/"}, 200
    else:
        print('nao ok')
        return {"erro": "Usuário ou senha inválidos"}, 401

# página de criar conta
@app.get('/criar-conta')
def criar_conta_get():
    if session.get("user_id"): #se ele ja ta logado ele tem uma conta
        return redirect("/")
    return render_template('criar_conta.html')

@app.post('/criar-conta')
def criar_conta_post():
    session.clear()
    dados = request.get_json()

    if not dados:
        return {"erro": "Dados não recebidos"}, 400

    usuario = dados.get('usuario', '').strip()
    senha = dados.get('senha', '')
    senha_confirma = dados.get('senha_confirma', '')

    if not usuario or not senha:
        return {"erro": "Usuário e senha são obrigatórios"}, 400

    if senha != senha_confirma:
        return {"erro": "As senhas não coincidem"}, 400

    db = get_db()
    usuario_existente = db.execute(
        "SELECT usuario FROM usuarios WHERE usuario = ?", (usuario,)
    ).fetchone()

    if usuario_existente:
        return {"erro": "Esse nome de usuário já está em uso."}, 400

    hash_senha = generate_password_hash(senha)
    db.execute(
        "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, hash_senha)
    )
    db.commit()

    return {"redirect": "/login"}, 200

# logout
@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
