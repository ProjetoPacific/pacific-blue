<<<<<<< HEAD
# faz o login, cadastro e troca de senha do sistema
=======
#faz login, cadastro, troca de senha e saida do sistema
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

from flask import Blueprint, render_template, request, redirect, url_for, session
from dados import usuarios

login_bp = Blueprint("login", __name__)


@login_bp.route("/", methods=["GET", "POST"])
def login():
    erro = None
<<<<<<< HEAD

=======
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        encontrado = False
        for u in usuarios:
            if u["usuario"] == usuario and u["senha"] == senha:
                session["usuario"] = u["nome"]
<<<<<<< HEAD
                session["usuario_login"] = u["usuario"]
=======
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
                encontrado = True

        if encontrado:
            return redirect(url_for("dashboard.dashboard"))
<<<<<<< HEAD

        erro = "Usuário ou senha inválidos!"
=======
        else:
            erro = "Usuário ou senha inválidos!"
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

    return render_template("login.html", erro=erro)


@login_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None
    sucesso = None

    if request.method == "POST":
<<<<<<< HEAD
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
=======
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
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
            else:
                usuarios.append({
                    "usuario": usuario,
                    "senha": senha,
                    "nome": nome,
<<<<<<< HEAD
                    "email": email
                })
                sucesso = "Conta criada com sucesso!"
=======
                    "email": email,
                })
                sucesso = "Conta criada com sucesso! Você já pode entrar."
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

    return render_template("cadastro.html", erro=erro, sucesso=sucesso)


@login_bp.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    erro = None
    sucesso = None

    if request.method == "POST":
<<<<<<< HEAD
        usuario = request.form.get("usuario")
        email = request.form.get("email")
=======
        usuario = request.form.get("usuario").strip()
        email = request.form.get("email").strip()
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
        nova_senha = request.form.get("nova_senha")
        confirmar = request.form.get("confirmar")

        encontrado = None
        for u in usuarios:
<<<<<<< HEAD
            if u["usuario"] == usuario and u["email"] == email:
                encontrado = u

        if encontrado is None:
            erro = "Usuário ou e-mail não encontrados!"
        elif nova_senha != confirmar:
            erro = "As senhas não são iguais!"
        else:
            encontrado["senha"] = nova_senha
            sucesso = "Senha alterada com sucesso!"
=======
            if u["usuario"].lower() == usuario.lower() and u.get("email", "").lower() == email.lower():
                encontrado = u

        if encontrado is None:
            erro = "Usuário e e-mail não conferem."
        elif nova_senha != confirmar:
            erro = "As senhas não são iguais."
        else:
            encontrado["senha"] = nova_senha
            sucesso = "Senha alterada com sucesso! Agora você pode entrar."
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

    return render_template("esqueci_senha.html", erro=erro, sucesso=sucesso)


<<<<<<< HEAD
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
=======
@login_bp.route("/sair")
def sair():
    session.pop("usuario", None)
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
    return redirect(url_for("login.login"))
