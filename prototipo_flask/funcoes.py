from functools import wraps
from flask import redirect, render_template, session

# este arquivo foi criado para armazenar funções auxiliares

# protege paginas que precisam de login
def login_required(funcao):
    @wraps(funcao)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return funcao(*args, **kwargs)

    return decorated_function