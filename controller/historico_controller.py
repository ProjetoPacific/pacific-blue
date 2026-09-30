#mostra o que ja aconteceu no estoque

from flask import Blueprint, render_template, request, session, redirect, url_for
from dados import movimentacoes

historico_bp = Blueprint("historico", __name__)


@historico_bp.route("/historico")
def historico():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    busca = request.args.get("busca", "")
    lista = []
    for m in movimentacoes:
        if busca.lower() in m["produto"].lower():
            lista.append(m)

    return render_template("historico.html", movimentacoes=lista, busca=busca)
