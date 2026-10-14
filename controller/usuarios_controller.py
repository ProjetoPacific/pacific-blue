# mostra os usuarios do sistema

from flask import Blueprint, render_template, session, redirect, url_for
from dados import usuarios

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios")
def usuarios_lista():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    return render_template("usuarios.html", usuarios=usuarios)
