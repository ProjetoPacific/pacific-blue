<<<<<<< HEAD
# mostra os usuarios do sistema

from flask import Blueprint, render_template, session, redirect, url_for
=======
#mostra usuarios e permite trocar senhas

from flask import Blueprint, render_template, request, redirect, url_for, session
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
from dados import usuarios

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios")
def usuarios_lista():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    return render_template("usuarios.html", usuarios=usuarios)
<<<<<<< HEAD
=======


@usuarios_bp.route("/usuarios/senha", methods=["GET", "POST"])
def alterar_senha():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    erro = None
    sucesso = None

    if request.method == "POST":
        senha_atual = request.form.get("senha_atual")
        nova_senha = request.form.get("nova_senha")
        confirmar = request.form.get("confirmar")

        encontrado = None
        for u in usuarios:
            if u["nome"] == session["usuario"]:
                encontrado = u

        if encontrado is None or encontrado["senha"] != senha_atual:
            erro = "Senha atual inválida."
        elif nova_senha != confirmar:
            erro = "As senhas não são iguais."
        else:
            encontrado["senha"] = nova_senha
            sucesso = "Senha alterada com sucesso!"

    return render_template("alterar_senha.html", erro=erro, sucesso=sucesso)
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
