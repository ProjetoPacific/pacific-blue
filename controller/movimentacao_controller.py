# coloca ou retira produtos do estoque e registra o histórico

from flask import Blueprint, render_template, request, redirect, url_for, session
from dados import movimentacoes, produtos, clientes, fornecedores, locais, origens_movimentacao

movimentacao_bp = Blueprint("movimentacao", __name__)


@movimentacao_bp.route("/movimentacao", methods=["GET", "POST"])
def movimentacao():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    tipo = request.args.get("tipo", "Entrada")
    if tipo not in ["Entrada", "Saída"]:
        tipo = "Entrada"

    erro = None

    if request.method == "POST":
        tipo_form = request.form.get("tipo")
        produto = request.form.get("produto")
        quantidade_texto = request.form.get("quantidade")
        data = request.form.get("data")
        origem = request.form.get("origem")
        local = request.form.get("local")

        try:
            quantidade = int(quantidade_texto)
        except (TypeError, ValueError):
            quantidade = 0
            erro = "Digite uma quantidade válida."

        if erro is None and tipo_form not in origens_movimentacao:
            erro = "Tipo de movimentação inválido."

        if erro is None and quantidade <= 0:
            erro = "A quantidade deve ser maior que zero."

        if erro is None and origem not in origens_movimentacao.get(tipo_form, []):
            erro = "Selecione uma origem válida para esse tipo de movimentação."

        produto_encontrado = None
        if erro is None:
            for p in produtos:
                if p["referencia"] == produto:
                    produto_encontrado = p
                    break

            if produto_encontrado is None:
                erro = "Produto não encontrado."

        if erro is None and tipo_form == "Saída" and produto_encontrado["estoque"] < quantidade:
            erro = "A quantidade de saída é maior que o estoque disponível."

        if erro is None:
            quantidade_movimentada = quantidade
            if tipo_form == "Saída":
                quantidade_movimentada = -quantidade

            produto_encontrado["estoque"] += quantidade_movimentada

            movimentacao_nova = {
                "data": data,
                "produto": produto,
                "tipo": tipo_form,
                "origem": origem,
                "doc_origem": request.form.get("doc_origem", ""),
                "fornecedor": request.form.get("fornecedor", ""),
                "quantidade": quantidade_movimentada,
                "local": local,
                "doc_destino": request.form.get("doc_destino", ""),
                "cliente": request.form.get("cliente", ""),
                "usuario": session["usuario"],
                "observacao": request.form.get("observacao", ""),
            }
            movimentacoes.append(movimentacao_nova)
            return redirect(url_for("historico.historico"))

    nomes_clientes = []
    for c in clientes:
        nomes_clientes.append(c["nome"])

    return render_template(
        "movimentacao.html",
        tipo=tipo,
        produtos=produtos,
        clientes=nomes_clientes,
        fornecedores=fornecedores,
        locais=locais,
        origens=origens_movimentacao.get(tipo, []),
        erro=erro,
    )


# planilhas separadas para consultar as entradas e as saídas registradas
@movimentacao_bp.route("/entradas")
def entradas():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    lista = []
    for m in movimentacoes:
        if m.get("tipo") == "Entrada":
            lista.append(m)

    return render_template("entradas.html", movimentacoes=lista)


@movimentacao_bp.route("/saidas")
def saidas():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    lista = []
    for m in movimentacoes:
        if m.get("tipo") == "Saída":
            lista.append(m)

    return render_template("saidas.html", movimentacoes=lista)
