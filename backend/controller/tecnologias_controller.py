from flask import Blueprint, render_template, session, redirect, url_for

tecnologias_bp = Blueprint("tecnologias", __name__)

@tecnologias_bp.route("/tecnologias")
def tecnologias():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    return render_template("tecnologias.html")