# mostra os usuarios do sistema

from flask import Blueprint, render_template, session, redirect, url_for
from banco import consultar

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios")
def usuarios_lista():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    usuarios = consultar("SELECT usuario, nome, email FROM usuarios ORDER BY id")
    return render_template("usuarios.html", usuarios=usuarios)
