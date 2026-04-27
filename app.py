from flask import Flask, render_template, request, session, g, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import sqlite3
from boole import run_boole

from funcoes import login_required, get_db, salvar_duvida, obter_duvida, obter_historico, criar_id, receber_duvidas_chat

# ============= CONFIGURAÇÃO =============

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# ============= BANCO DE DADOS =============
@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# ============= ROTAS =============
# página inicial
@app.get("/")
def index_get():
    return render_template("index.html")

@app.post("/")
def index_post():
    dados = request.get_json()
    if not dados:
        return {"erro": "Dados não recebidos"}, 400

    num = dados.get('num') # número de perguntas já feitas
    duvida = dados.get('duvida', '').strip()
    if not duvida:
        return {"erro": "Dúvida não pode estar vazia"}, 400

    resultados = run_boole(duvida, num)
    resposta_boole = resultados[0]
    titulo = resultados[1] 

    # caso seja a primeira mensagem, cria um id pro chat
    if num <= 2:
        id_chat = criar_id()

    else:
        # caso contrario, pega ultimo id
        db = get_db()
        cursor = db.execute(
            "SELECT id_chat FROM duvidas WHERE id = (SELECT MAX(id) FROM duvidas);"
        )
        resultado = cursor.fetchone()
        id_chat_dict = dict(resultado)
        id_chat = id_chat_dict['id_chat']

    usuario = session.get("user_id")
    salvar_duvida(usuario, duvida, resposta_boole, titulo, id_chat)

    # recebe duvidas do chat
    duvida = receber_duvidas_chat(id_chat)
    print(duvida)

    return {"resultado": resposta_boole, "titulo": titulo}, 200

@app.get("/historico")
def obter_historico_route():
    usuario, erro = checar_autenticacao()
    if erro:
        return erro

    return {"duvidas": obter_historico(usuario)}, 200

@app.get("/historico/<int:duvida_id>")
def obter_duvida_route(duvida_id):
    usuario, erro = checar_autenticacao()
    if erro:
        return erro

    duvida = obter_duvida(usuario, duvida_id)
    if not duvida:
        return {"erro": "Dúvida não encontrada"}, 404

    return duvida, 200

@app.post('/continuar-sem-login')
def continuar_sem_login():
    session.clear()
    session["anonymous"] = True
    return {"redirect": "/"}, 200

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

    usuario = dados.get('usuario', '').strip()
    senha = dados.get('senha', '')

    if not usuario or not senha:
        return {"erro": "Usuário e senha são obrigatórios"}, 400

    row = get_db().execute(
        "SELECT senha FROM usuarios WHERE usuario = ?", (usuario,)
    ).fetchone()

    if row and check_password_hash(row["senha"], senha):
        session["user_id"] = usuario
        session.pop("anonymous", None)
        return {"redirect": "/"}, 200
    else:
        print('nao ok')
        return {"erro": "Usuário ou senha inválidos"}, 401

@app.get('/criar-conta')
def criar_conta_get():
    if session.get("user_id"):
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
    if db.execute(
        "SELECT 1 FROM usuarios WHERE usuario = ?", (usuario,)
    ).fetchone():
        return {"erro": "Esse nome de usuário já está em uso."}, 400

    db.execute(
        "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
        (usuario, generate_password_hash(senha))
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