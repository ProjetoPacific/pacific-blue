#cadastra e procura produtos

from flask import Blueprint, render_template, request, redirect, url_for, session
from dados import produtos, clientes, grupos, generos

produtos_bp = Blueprint("produtos", __name__)


@produtos_bp.route("/produtos")
def produtos_lista():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    busca = request.args.get("busca", "")
    grupo = request.args.get("grupo", "Todos")
    cliente = request.args.get("cliente", "Todos")
    status = request.args.get("status", "Todos")

    lista = []
    for p in produtos:
        texto = " ".join([
            p.get("referencia", ""), p.get("nome", ""), p.get("grupo", ""),
            p.get("cliente", ""), p.get("descricao", "")
        ]).lower()
        if busca.lower() not in texto:
            continue
        if grupo != "Todos" and p.get("grupo") != grupo:
            continue
        if cliente != "Todos" and p.get("cliente") != cliente:
            continue

        status_produto = "Baixo" if p["estoque"] <= p["estoque_minimo"] else "OK"
        if status != "Todos" and status_produto != status:
            continue

        lista.append(p)

    nomes_clientes = []
    for c in clientes:
        nomes_clientes.append(c["nome"])

    return render_template(
        "produtos.html",
        produtos=lista,
        busca=busca,
        grupo=grupo,
        cliente=cliente,
        status=status,
        grupos=grupos,
        clientes=nomes_clientes,
    )


@produtos_bp.route("/produtos/novo", methods=["GET", "POST"])
def novo_produto():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    if request.method == "POST":
        produto = {
            "referencia": request.form.get("referencia"),
            "ncm": request.form.get("ncm"),
            "nome": request.form.get("nome"),
            "descricao": request.form.get("descricao"),
            "grupo": request.form.get("grupo"),
            "estilo": request.form.get("estilo"),
            "cliente": request.form.get("cliente"),
            "genero": request.form.get("genero"),
            "cor": request.form.get("cor"),
            "tamanhos": request.form.get("tamanhos"),
            "tecido": request.form.get("tecido"),
            "composicao": request.form.get("composicao"),
            "estoque": 0,
            "estoque_minimo": 10,
            "data_estoque": request.form.get("data_estoque"),
        }
        produtos.append(produto)
        return redirect(url_for("produtos.produtos_lista"))

    nomes_clientes = []
    for c in clientes:
        nomes_clientes.append(c["nome"])

    return render_template(
        "cadastrar_produto.html",
        grupos=grupos,
        generos=generos,
        clientes=nomes_clientes,
    )
