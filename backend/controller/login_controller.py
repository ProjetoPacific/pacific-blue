# faz o login, cadastro e troca de senha do sistema

from flask import Blueprint, render_template, request, redirect, url_for, session
from banco import consultar_um, transacao

login_bp = Blueprint("login", __name__)


@login_bp.route("/", methods=["GET", "POST"])
def login():
    erro = None

    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        encontrado = consultar_um(
            "SELECT usuario, nome FROM usuarios WHERE usuario = ? AND senha = ?",
            (usuario, senha),
        )

        if encontrado:
            session["usuario"] = encontrado["nome"]
            session["usuario_login"] = encontrado["usuario"]
            return redirect(url_for("dashboard.dashboard"))

        erro = "Usuário ou senha inválidos!"

    return render_template("login.html", erro=erro)


@login_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None
    sucesso = None

    if request.method == "POST":
        nome = request.form.get("nome", "")
        email = request.form.get("email", "")
        usuario = request.form.get("usuario", "")
        senha = request.form.get("senha", "")
        confirmar = request.form.get("confirmar")

        if not usuario or not senha or not nome:
            erro = "Preencha nome, usuário e senha!"
        elif senha != confirmar:
            erro = "As senhas não são iguais!"
        elif consultar_um("SELECT 1 FROM usuarios WHERE usuario = ?", (usuario,)):
            erro = "Esse usuário já existe!"
        else:
            with transacao() as db:
                db.execute(
                    "INSERT INTO usuarios (usuario, senha, nome, email) VALUES (?, ?, ?, ?)",
                    (usuario, senha, nome, email),
                )
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

        encontrado = consultar_um(
            "SELECT id FROM usuarios WHERE usuario = ? AND email = ?", (usuario, email)
        )

        if encontrado is None:
            erro = "Usuário ou e-mail não encontrados!"
        elif nova_senha != confirmar:
            erro = "As senhas não são iguais!"
        else:
            with transacao() as db:
                db.execute("UPDATE usuarios SET senha = ? WHERE id = ?", (nova_senha, encontrado["id"]))
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

        usuario_atual = consultar_um(
            "SELECT id, senha FROM usuarios WHERE usuario = ?", (session.get("usuario_login"),)
        )

        if usuario_atual is None or usuario_atual["senha"] != senha_atual:
            erro = "Senha atual inválida!"
        elif nova_senha != confirmar:
            erro = "As senhas não são iguais!"
        else:
            with transacao() as db:
                db.execute("UPDATE usuarios SET senha = ? WHERE id = ?", (nova_senha, usuario_atual["id"]))
            sucesso = "Senha alterada com sucesso!"

    return render_template("alterar_senha.html", erro=erro, sucesso=sucesso)


@login_bp.route("/sair")
def sair():
    session.pop("usuario", None)
    session.pop("usuario_login", None)
    return redirect(url_for("login.login"))
