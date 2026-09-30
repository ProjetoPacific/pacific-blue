#coloca, tira ou ajusta produtos no estoque

from flask import Blueprint, render_template, request, redirect, url_for, session
from dados import movimentacoes, produtos, motivos_movimentacao

movimentacao_bp = Blueprint("movimentacao", __name__)


@movimentacao_bp.route("/movimentacao", methods=["GET", "POST"])
def movimentacao():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    tipo = request.args.get("tipo", "Entrada")
    if tipo not in motivos_movimentacao:
        tipo = "Entrada"

    erro = None
    if request.method == "POST":
        produto = request.form.get("produto")
        quantidade_texto = request.form.get("quantidade")
        tipo_form = request.form.get("tipo")
        motivo = request.form.get("motivo")
        data = request.form.get("data")
        observacao = request.form.get("observacao")

        try:
            quantidade = int(quantidade_texto)
        except (TypeError, ValueError):
            quantidade = 0
            erro = "Digite uma quantidade válida."

        if erro is None and quantidade <= 0:
            erro = "A quantidade deve ser maior que zero."

        if erro is None and motivo not in motivos_movimentacao.get(tipo_form, []):
            erro = "O motivo selecionado não é válido para esse tipo de movimentação."

        produto_encontrado = None
        if erro is None:
            for p in produtos:
                if p["referencia"] == produto:
                    produto_encontrado = p

            if produto_encontrado is None:
                erro = "Produto não encontrado."

        if erro is None:
            quantidade_movimentada = quantidade
            if tipo_form == "Saída":
                if produto_encontrado["estoque"] < quantidade:
                    erro = "A quantidade de saída é maior que o estoque disponível."
                else:
                    quantidade_movimentada = -quantidade
            elif tipo_form == "Ajuste":
                sinal = request.form.get("sinal_ajuste", "entrada")
                if sinal == "saida":
                    if produto_encontrado["estoque"] < quantidade:
                        erro = "O ajuste de saída é maior que o estoque disponível."
                    else:
                        quantidade_movimentada = -quantidade

        if erro is None:
            produto_encontrado["estoque"] += quantidade_movimentada
            movimentacoes.append({
                "data": data,
                "produto": produto,
                "tipo": tipo_form,
                "motivo": motivo,
                "quantidade": quantidade_movimentada,
                "usuario": session["usuario"],
                "observacao": observacao,
            })
            return redirect(url_for("dashboard.dashboard"))

    return render_template(
        "movimentacao.html",
        tipo=tipo,
        produtos=produtos,
        motivos=motivos_movimentacao.get(tipo, []),
        erro=erro,
    )
