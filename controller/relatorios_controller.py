#prepara as informacoes para os relatorios

from flask import Blueprint, render_template, session, redirect, url_for
from dados import produtos, movimentacoes, lotes, ordens

relatorios_bp = Blueprint("relatorios", __name__)


def acesso():
    if "usuario" not in session:
        return redirect(url_for("login.login"))
    return None


@relatorios_bp.route("/relatorios")
def relatorios():
    bloqueio = acesso()
    if bloqueio:
        return bloqueio

    total_produtos = 0
    for p in produtos:
        total_produtos += p["estoque"]

    estoque_minimo = 0
    for p in produtos:
        if p["estoque"] <= p["estoque_minimo"]:
            estoque_minimo += 1

    return render_template(
        "relatorios.html",
        total_produtos=total_produtos,
        estoque_minimo=estoque_minimo,
        total_lotes=len(lotes),
        total_movimentacoes=len(movimentacoes),
    )


@relatorios_bp.route("/relatorios/estoque")
def relatorio_estoque():
    bloqueio = acesso()
    if bloqueio:
        return bloqueio
    return render_template("relatorio_estoque.html", produtos=produtos)


@relatorios_bp.route("/relatorios/movimentacoes")
def relatorio_movimentacoes():
    bloqueio = acesso()
    if bloqueio:
        return bloqueio
    return render_template("relatorio_movimentacoes.html", movimentacoes=movimentacoes)


@relatorios_bp.route("/relatorios/estoque-minimo")
def relatorio_estoque_minimo():
    bloqueio = acesso()
    if bloqueio:
        return bloqueio

    produtos_baixos = []
    for p in produtos:
        if p["estoque"] <= p["estoque_minimo"]:
            produtos_baixos.append(p)

    return render_template("relatorio_estoque_minimo.html", produtos=produtos_baixos)


@relatorios_bp.route("/relatorios/lotes")
def relatorio_lotes():
    bloqueio = acesso()
    if bloqueio:
        return bloqueio
    return render_template("relatorio_lotes.html", lotes=lotes)
