<<<<<<< HEAD
# coloca ou retira produtos do estoque e registra o histórico

from flask import Blueprint, render_template, request, redirect, url_for, session
from dados import movimentacoes, produtos, clientes, fornecedores, locais, origens_movimentacao
=======
#coloca, tira ou ajusta produtos no estoque

from flask import Blueprint, render_template, request, redirect, url_for, session
from dados import movimentacoes, produtos, motivos_movimentacao
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

movimentacao_bp = Blueprint("movimentacao", __name__)


@movimentacao_bp.route("/movimentacao", methods=["GET", "POST"])
def movimentacao():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    tipo = request.args.get("tipo", "Entrada")
<<<<<<< HEAD
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
=======
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
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

        try:
            quantidade = int(quantidade_texto)
        except (TypeError, ValueError):
            quantidade = 0
            erro = "Digite uma quantidade válida."

<<<<<<< HEAD
        if erro is None and tipo_form not in origens_movimentacao:
            erro = "Tipo de movimentação inválido."

        if erro is None and quantidade <= 0:
            erro = "A quantidade deve ser maior que zero."

        if erro is None and origem not in origens_movimentacao.get(tipo_form, []):
            erro = "Selecione uma origem válida para esse tipo de movimentação."
=======
        if erro is None and quantidade <= 0:
            erro = "A quantidade deve ser maior que zero."

        if erro is None and motivo not in motivos_movimentacao.get(tipo_form, []):
            erro = "O motivo selecionado não é válido para esse tipo de movimentação."
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

        produto_encontrado = None
        if erro is None:
            for p in produtos:
                if p["referencia"] == produto:
                    produto_encontrado = p
<<<<<<< HEAD
                    break
=======
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

            if produto_encontrado is None:
                erro = "Produto não encontrado."

<<<<<<< HEAD
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
=======
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
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

    return render_template(
        "movimentacao.html",
        tipo=tipo,
        produtos=produtos,
<<<<<<< HEAD
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
=======
        motivos=motivos_movimentacao.get(tipo, []),
        erro=erro,
    )
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
