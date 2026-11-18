from flask import Blueprint, render_template, session, redirect, url_for
from banco import consultar, consultar_um

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if "usuario" not in session: return redirect(url_for("login.login"))

    estoque = consultar_um("SELECT COUNT(*) AS produtos, COALESCE(SUM(estoque), 0) AS pecas FROM produtos")
    produtos_em_falta = consultar(
        "SELECT referencia, descricao, estoque, estoque_minimo FROM produtos "
        "WHERE estoque <= estoque_minimo ORDER BY id"
    )
    totais = consultar_um(
        "SELECT "
        "COALESCE(SUM(CASE WHEN tipo = 'Entrada' THEN ABS(quantidade) END), 0) AS entradas, "
        "COALESCE(SUM(CASE WHEN tipo = 'Saída'   THEN ABS(quantidade) END), 0) AS saidas "
        "FROM movimentacoes"
    )
    ordens_paradas = consultar_um(
        "SELECT COUNT(DISTINCT ordem_id) AS total FROM ordens_processos WHERE LOWER(processo) = 'parado'"
    )["total"]
    ultimas = consultar(
        "SELECT data, produto, tipo, quantidade, usuario FROM movimentacoes ORDER BY id DESC LIMIT 6"
    )

    return render_template("dashboard.html", usuario=session["usuario"],
        total_produtos=estoque["produtos"], total_pecas=estoque["pecas"],
        produtos_baixos=len(produtos_em_falta), total_entradas=totais["entradas"],
        total_saidas=totais["saidas"], ordens_paradas=ordens_paradas,
        movimentacoes=ultimas, produtos_em_falta=produtos_em_falta)
