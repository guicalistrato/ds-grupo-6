from flask import Flask, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import sqlite3
from boole import run_boole

from funcoes import login_required
# configuração inicial
app = Flask(__name__)

# armazena os dados no servidor ao inves dos cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# garante que usuario nao consiga acessar versoes antigas
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# pagina inicial
@app.get("/")
@login_required
def index_get():
    return render_template("index.html")

@app.post("/")
@login_required
def index_post():
    dados = request.get_json()
    print(dados)
    if not dados:
        return {"erro": "Dados não recebidos"}, 400
    
    # recebe pergunta e roda função para boole gerar resposta
    duvida = dados.get('duvida')
    resposta_boole = run_boole(duvida)
    print(resposta_boole)

    # armazena respostas no histórico
    with sqlite3.connect('dados.db') as conn:
        db = conn.cursor()
        db.execute("INSERT INTO historico (usuario, pergunta, resposta) VALUES (?, ?, ?);", (session["user_id"], duvida, resposta_boole))

        conn.commit()

    # retorna o resultado em forma de json
    return {"resultado": resposta_boole}, 200

# página de login
@app.get('/login')
def login_get():
    session.clear()
    return render_template('login.html')

@app.post('/login')
def login_post():
    session.clear()
    # recebe os dados do javascript
    dados = request.get_json()
    
    if not dados:
        return {"erro": "Dados não recebidos"}, 400 
        
    usuario = dados.get('usuario')
    senha = dados.get('senha')

    # checa se os dados batem
    with sqlite3.connect('dados.db') as conn:
        db = conn.cursor()
        db.execute("SELECT senha FROM usuarios WHERE usuario = ?", (usuario,))
        senha_db = db.fetchone()

    if senha_db and check_password_hash(senha_db[0], senha):
        session["user_id"] = usuario
        print('ok')
        return {"redirect": "/"}, 200
    else:
        print('nao ok')

# página de criar conta
@app.get('/criar-conta')
def criar_conta_get():
    session.clear()
    return render_template('criar_conta.html')

@app.post('/criar-conta')
def criar_conta_post():
    session.clear()
    # recebe os dados pelo json
    dados = request.get_json()
    
    if not dados:
        return "Erro: Dados não recebidos", 400
        
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    senha_confirma = dados.get('senha_confirma')

    print(f'DEBUG: usuario : {usuario}, senha : {senha}, senha2 : {senha_confirma}')

    # checa se as senhas sao iguais
    if senha == senha_confirma:
        hash = generate_password_hash(senha)

        # guarda usuario e senha no banco de dados
        with sqlite3.connect('dados.db') as conn:
            db = conn.cursor()

            # checa se o usuario ja existe
            db.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (usuario,))
            usuario_existente = db.fetchone()

            # se sim, retorna o erro
            if usuario_existente:
                return {"erro": "Esse nome de usuário já está em uso."}, 400

            else:
                db.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?);", (usuario, hash))
                conn.commit()
        
        # redireciona para a tela de login
        return {"redirect": "/login"}, 400

    # se as senhas forem diferentes, retorna para a parte de criar conta
    else:
        return {"redirect": "/criar-conta"}, 200