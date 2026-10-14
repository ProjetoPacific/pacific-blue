#pega informacoes e mostra no dashboard

from flask import Blueprint, render_template, session, redirect, url_for
from dados import produtos, movimentacoes, lotes

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    total_produtos = 0
    for p in produtos:
        total_produtos += p["estoque"]

    produtos_em_falta = []
    for p in produtos:
        if p["estoque"] <= p["estoque_minimo"]:
            produtos_em_falta.append(p)

    lotes_lavanderia = 0
    for l in lotes:
        if l["status"] == "Em Lavanderia":
            lotes_lavanderia += 1

    ultimas_movimentacoes = movimentacoes[-5:]

    return render_template(
        "dashboard.html",
        usuario=session["usuario"],
        total_produtos=total_produtos,
        estoque_minimo=len(produtos_em_falta),
        lotes_lavanderia=lotes_lavanderia,
        movimentacoes=ultimas_movimentacoes,
        produtos_em_falta=produtos_em_falta,
    )
