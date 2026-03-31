from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import sqlite3

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
@app.route("/")
#@login_required
def index():
    conn = sqlite3.connect('dados.db')
    db = conn.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usuarios (" \
    "usuario text," \
    "senha text" \
    ");")
    db.execute("SELECT * FROM usuarios")
    dados = db.fetchall()
    conn.close()
    return render_template("index.html", dados=dados)

@app.route("/login")
def login():
    # apagar dados antigos
    session.clear()

