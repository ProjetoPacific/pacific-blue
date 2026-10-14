<<<<<<< HEAD
# cadastra, procura e mostra produtos

from flask import Blueprint, render_template, request, redirect, url_for, session
from dados import produtos, clientes, fornecedores, grupos, generos
=======
#cadastra e procura produtos

from flask import Blueprint, render_template, request, redirect, url_for, session
from dados import produtos, clientes, grupos, generos
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

produtos_bp = Blueprint("produtos", __name__)


@produtos_bp.route("/produtos")
def produtos_lista():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    busca = request.args.get("busca", "")
    grupo = request.args.get("grupo", "Todos")
    cliente = request.args.get("cliente", "Todos")
<<<<<<< HEAD
=======
    status = request.args.get("status", "Todos")
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

    lista = []
    for p in produtos:
        texto = " ".join([
<<<<<<< HEAD
            p.get("referencia", ""), p.get("descricao", ""), p.get("cor", ""),
            p.get("tamanho", ""), p.get("genero", ""), p.get("grupo", ""),
            p.get("grade", ""), p.get("cliente", ""), p.get("fornecedor", "")
        ]).lower()

=======
            p.get("referencia", ""), p.get("nome", ""), p.get("grupo", ""),
            p.get("cliente", ""), p.get("descricao", "")
        ]).lower()
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
        if busca.lower() not in texto:
            continue
        if grupo != "Todos" and p.get("grupo") != grupo:
            continue
        if cliente != "Todos" and p.get("cliente") != cliente:
            continue

<<<<<<< HEAD
=======
        status_produto = "Baixo" if p["estoque"] <= p["estoque_minimo"] else "OK"
        if status != "Todos" and status_produto != status:
            continue

>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
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
<<<<<<< HEAD
=======
        status=status,
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
        grupos=grupos,
        clientes=nomes_clientes,
    )


@produtos_bp.route("/produtos/novo", methods=["GET", "POST"])
def novo_produto():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

<<<<<<< HEAD
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
=======
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
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

    nomes_clientes = []
    for c in clientes:
        nomes_clientes.append(c["nome"])

    return render_template(
        "cadastrar_produto.html",
        grupos=grupos,
        generos=generos,
        clientes=nomes_clientes,
<<<<<<< HEAD
        fornecedores=fornecedores,
        erro=erro,
=======
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
    )
