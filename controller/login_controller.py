# faz o login, cadastro e troca de senha do sistema

from flask import Blueprint, render_template, request, redirect, url_for, session
from dados import usuarios

login_bp = Blueprint("login", __name__)


@login_bp.route("/", methods=["GET", "POST"])
def login():
    erro = None

    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        encontrado = False
        for u in usuarios:
            if u["usuario"] == usuario and u["senha"] == senha:
                session["usuario"] = u["nome"]
                session["usuario_login"] = u["usuario"]
                encontrado = True

        if encontrado:
            return redirect(url_for("dashboard.dashboard"))

        erro = "Usuário ou senha inválidos!"

    return render_template("login.html", erro=erro)


@login_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None
    sucesso = None

    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        confirmar = request.form.get("confirmar")

        if senha != confirmar:
            erro = "As senhas não são iguais!"
        else:
            existe = False
            for u in usuarios:
                if u["usuario"] == usuario:
                    existe = True

            if existe:
                erro = "Esse usuário já existe!"
            else:
                usuarios.append({
                    "usuario": usuario,
                    "senha": senha,
                    "nome": nome,
                    "email": email
                })
                sucesso = "Conta criada com sucesso!"

    return render_template("cadastro.html", erro=erro, sucesso=sucesso)


@login_bp.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    erro = None
    sucesso = None

    if request.method == "POST":
        usuario = request.form.get("usuario")
        email = request.form.get("email")
        nova_senha = request.form.get("nova_senha")
        confirmar = request.form.get("confirmar")

        encontrado = None
        for u in usuarios:
            if u["usuario"] == usuario and u["email"] == email:
                encontrado = u

        if encontrado is None:
            erro = "Usuário ou e-mail não encontrados!"
        elif nova_senha != confirmar:
            erro = "As senhas não são iguais!"
        else:
            encontrado["senha"] = nova_senha
            sucesso = "Senha alterada com sucesso!"

    return render_template("esqueci_senha.html", erro=erro, sucesso=sucesso)


@login_bp.route("/alterar-senha", methods=["GET", "POST"])
def alterar_senha():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    erro = None
    sucesso = None

    if request.method == "POST":
        senha_atual = request.form.get("senha_atual")
        nova_senha = request.form.get("nova_senha")
        confirmar = request.form.get("confirmar")

        usuario_atual = None
        for u in usuarios:
            if u["usuario"] == session.get("usuario_login"):
                usuario_atual = u

        if usuario_atual is None or usuario_atual["senha"] != senha_atual:
            erro = "Senha atual inválida!"
        elif nova_senha != confirmar:
            erro = "As senhas não são iguais!"
        else:
            usuario_atual["senha"] = nova_senha
            sucesso = "Senha alterada com sucesso!"

    return render_template("alterar_senha.html", erro=erro, sucesso=sucesso)


@login_bp.route("/sair")
def sair():
    session.pop("usuario", None)
    session.pop("usuario_login", None)
    return redirect(url_for("login.login"))
