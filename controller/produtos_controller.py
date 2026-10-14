# cadastra, procura e mostra produtos

from flask import Blueprint, render_template, request, redirect, url_for, session
from dados import produtos, clientes, fornecedores, grupos, generos

produtos_bp = Blueprint("produtos", __name__)


@produtos_bp.route("/produtos")
def produtos_lista():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    busca = request.args.get("busca", "")
    grupo = request.args.get("grupo", "Todos")
    cliente = request.args.get("cliente", "Todos")

    lista = []
    for p in produtos:
        texto = " ".join([
            p.get("referencia", ""), p.get("descricao", ""), p.get("cor", ""),
            p.get("tamanho", ""), p.get("genero", ""), p.get("grupo", ""),
            p.get("grade", ""), p.get("cliente", ""), p.get("fornecedor", "")
        ]).lower()

        if busca.lower() not in texto:
            continue
        if grupo != "Todos" and p.get("grupo") != grupo:
            continue
        if cliente != "Todos" and p.get("cliente") != cliente:
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
        grupos=grupos,
        clientes=nomes_clientes,
    )


@produtos_bp.route("/produtos/novo", methods=["GET", "POST"])
def novo_produto():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    erro = None

    if request.method == "POST":
        referencia = request.form.get("referencia").strip()

        existe = False
        for p in produtos:
            if p["referencia"].lower() == referencia.lower():
                existe = True

        if existe:
            erro = "Essa referência já está cadastrada."
        else:
            produto = {
                "referencia": referencia,
                "descricao": request.form.get("descricao").strip(),
                "cor": request.form.get("cor").strip(),
                "tamanho": request.form.get("tamanho").strip(),
                "genero": request.form.get("genero"),
                "grupo": request.form.get("grupo"),
                "grade": request.form.get("grade").strip(),
                "data": request.form.get("data").strip(),
                "cliente": request.form.get("cliente"),
                "fornecedor": request.form.get("fornecedor"),
                "estoque": 0,
                "estoque_minimo": 10,
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
        fornecedores=fornecedores,
        erro=erro,
    )
