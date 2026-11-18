# coloca ou retira produtos do estoque e registra o histórico

from flask import Blueprint, render_template, request, redirect, url_for, session
from banco import consultar, consultar_um, transacao

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
        local = request.form.get("local", "").strip()
        ordem_producao = request.form.get("ordem_producao", "").strip()
        cliente = request.form.get("cliente", "").strip()

        try:
            quantidade = int(quantidade_texto)
        except (TypeError, ValueError):
            quantidade = 0
            erro = "Digite uma quantidade válida."

        if erro is None and tipo_form not in ["Entrada", "Saída"]:
            erro = "Tipo de movimentação inválido."

        if erro is None and quantidade <= 0:
            erro = "A quantidade deve ser maior que zero."

        if erro is None and origem not in ["Entrada", "Saída"]:
            erro = "Selecione Entrada ou Saída como origem."
        if erro is None and not all([ordem_producao, cliente, local]):
            erro = "Informe a ordem de produção, o cliente e o processo."

        produto_encontrado = None
        if erro is None:
            produto_encontrado = consultar_um(
                "SELECT id, referencia, estoque FROM produtos WHERE referencia = ?", (produto,))

            if produto_encontrado is None:
                erro = "Produto não encontrado."

        if erro is None and tipo_form == "Saída" and produto_encontrado["estoque"] < quantidade:
            erro = "A quantidade de saída é maior que o estoque disponível."

        if erro is None:
            quantidade_movimentada = quantidade
            if tipo_form == "Saída":
                quantidade_movimentada = -quantidade

            # saldo e histórico são gravados juntos: ou os dois, ou nenhum
            with transacao() as db:
                atualizado = db.execute(
                    "UPDATE produtos SET estoque = estoque + ? WHERE id = ? AND estoque + ? >= 0",
                    (quantidade_movimentada, produto_encontrado["id"], quantidade_movimentada))
                if atualizado.rowcount == 0:
                    erro = "A quantidade de saída é maior que o estoque disponível."
                else:
                    db.execute(
                        "INSERT INTO movimentacoes (data, produto, tipo, origem, ordem_producao, doc_origem, "
                        "fornecedor, quantidade, local, doc_destino, cliente, usuario, observacao) "
                        "VALUES (?, ?, ?, ?, ?, ?, '', ?, ?, '', ?, ?, ?)",
                        (data or "", produto_encontrado["referencia"], tipo_form, origem, ordem_producao,
                         ordem_producao, quantidade_movimentada, local, cliente, session["usuario"],
                         request.form.get("observacao", "")))
            if erro is None:
                return redirect(url_for("historico.historico"))

    nomes_clientes = [c.get("nome_fantasia") or c.get("nome", "")
                      for c in consultar("SELECT nome_fantasia, nome FROM clientes ORDER BY id")]
    locais = ["used", "laser", "destroyed", "stone", "marmorizado", "tingimento", "amaciado", "parado"]
    produtos = consultar("SELECT referencia, descricao FROM produtos ORDER BY id")

    return render_template(
        "movimentacao.html",
        tipo=tipo,
        produtos=produtos,
        clientes=nomes_clientes,
        locais=locais,
        erro=erro,
    )


# planilhas separadas para consultar as entradas e as saídas registradas
@movimentacao_bp.route("/entradas")
def entradas():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    lista = consultar("SELECT * FROM movimentacoes WHERE tipo = 'Entrada' ORDER BY id", sem_nulos=True)
    return render_template("entradas.html", movimentacoes=lista)


@movimentacao_bp.route("/saidas")
def saidas():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    lista = consultar("SELECT * FROM movimentacoes WHERE tipo = 'Saída' ORDER BY id", sem_nulos=True)
    return render_template("saidas.html", movimentacoes=lista)
