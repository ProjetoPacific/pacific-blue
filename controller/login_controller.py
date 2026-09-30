#faz login, cadastro, troca de senha e saida do sistema

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
                encontrado = True

        if encontrado:
            return redirect(url_for("dashboard.dashboard"))
        else:
            erro = "Usuário ou senha inválidos!"

    return render_template("login.html", erro=erro)


@login_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None
    sucesso = None

    if request.method == "POST":
        usuario = request.form.get("usuario").strip()
        senha = request.form.get("senha")
        confirmar = request.form.get("confirmar")
        nome = request.form.get("nome").strip()
        email = request.form.get("email").strip()

        if senha != confirmar:
            erro = "As senhas não são iguais."
        else:
            existe = False
            for u in usuarios:
                if u["usuario"].lower() == usuario.lower():
                    existe = True

            if existe:
                erro = "Esse usuário já existe."
            else:
                usuarios.append({
                    "usuario": usuario,
                    "senha": senha,
                    "nome": nome,
                    "email": email,
                })
                sucesso = "Conta criada com sucesso! Você já pode entrar."

    return render_template("cadastro.html", erro=erro, sucesso=sucesso)


@login_bp.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    erro = None
    sucesso = None

    if request.method == "POST":
        usuario = request.form.get("usuario").strip()
        email = request.form.get("email").strip()
        nova_senha = request.form.get("nova_senha")
        confirmar = request.form.get("confirmar")

        encontrado = None
        for u in usuarios:
            if u["usuario"].lower() == usuario.lower() and u.get("email", "").lower() == email.lower():
                encontrado = u

        if encontrado is None:
            erro = "Usuário e e-mail não conferem."
        elif nova_senha != confirmar:
            erro = "As senhas não são iguais."
        else:
            encontrado["senha"] = nova_senha
            sucesso = "Senha alterada com sucesso! Agora você pode entrar."

    return render_template("esqueci_senha.html", erro=erro, sucesso=sucesso)


@login_bp.route("/sair")
def sair():
    session.pop("usuario", None)
    return redirect(url_for("login.login"))
