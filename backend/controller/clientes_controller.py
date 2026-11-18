from flask import Blueprint, render_template, request, redirect, url_for, session
from banco import consultar, consultar_um, transacao

clientes_bp = Blueprint("clientes", __name__)
CAMPOS = ("codigo","nome_fantasia","razao_social","endereco","telefone","cnpj","inscricao_estadual","transferencia","data")
COLUNAS = CAMPOS + ("nome", "email")  # "nome" e "email" existem por compatibilidade com telas antigas
SQL_COLUNAS = ", ".join(COLUNAS)

def dados_form():
    return {campo: request.form.get(campo, "").strip() for campo in CAMPOS}

@clientes_bp.route("/clientes")
def clientes_lista():
    if "usuario" not in session: return redirect(url_for("login.login"))
    busca = request.args.get("busca", "").casefold()
    lista = []
    for c in consultar(f"SELECT {SQL_COLUNAS} FROM clientes ORDER BY id"):
        texto = " ".join(str(c[k]) for k in COLUNAS).casefold()
        if busca in texto: lista.append(c)
    return render_template("clientes.html", clientes=lista, busca=busca, erro=request.args.get("erro"), sucesso=request.args.get("sucesso"))

@clientes_bp.route("/clientes/novo", methods=["GET","POST"])
def novo_cliente():
    if "usuario" not in session: return redirect(url_for("login.login"))
    erro = None
    if request.method == "POST":
        novo = dados_form()
        if not novo["codigo"] or not novo["nome_fantasia"] or not novo["razao_social"]:
            erro = "Preencha código, nome fantasia e razão social."
        elif consultar_um("SELECT 1 FROM clientes WHERE codigo = ?", (novo["codigo"],)):
            erro = "Esse código já está cadastrado."
        else:
            novo["nome"] = novo["nome_fantasia"]  # compatibilidade com telas antigas
            novo["email"] = ""
            with transacao() as db:
                db.execute(
                    f"INSERT INTO clientes ({SQL_COLUNAS}) VALUES ({', '.join('?' * len(COLUNAS))})",
                    tuple(novo[k] for k in COLUNAS),
                )
            return redirect(url_for("clientes.clientes_lista"))
    return render_template("novo_cliente.html", cliente=None, erro=erro)

@clientes_bp.route("/clientes/<codigo>/editar", methods=["GET","POST"])
def editar_cliente(codigo):
    if "usuario" not in session: return redirect(url_for("login.login"))
    cliente = consultar_um(f"SELECT id, {SQL_COLUNAS} FROM clientes WHERE codigo = ?", (codigo,))
    if cliente is None: return redirect(url_for("clientes.clientes_lista"))
    erro = None
    if request.method == "POST":
        atualizado = dados_form()
        if not atualizado["codigo"] or not atualizado["nome_fantasia"] or not atualizado["razao_social"]:
            erro = "Preencha código, nome fantasia e razão social."
        elif consultar_um("SELECT 1 FROM clientes WHERE codigo = ? AND id <> ?", (atualizado["codigo"], cliente["id"])):
            erro = "Esse código já está cadastrado."
        else:
            atualizado["nome"] = atualizado["nome_fantasia"]
            campos = CAMPOS + ("nome",)
            with transacao() as db:
                db.execute(
                    f"UPDATE clientes SET {', '.join(c + ' = ?' for c in campos)} WHERE id = ?",
                    tuple(atualizado[c] for c in campos) + (cliente["id"],),
                )
            return redirect(url_for("clientes.clientes_lista"))
    return render_template("novo_cliente.html", cliente=cliente, erro=erro)

@clientes_bp.route("/clientes/<codigo>/excluir", methods=["POST"])
def excluir_cliente(codigo):
    if "usuario" not in session: return redirect(url_for("login.login"))
    cliente = consultar_um(f"SELECT id, {SQL_COLUNAS} FROM clientes WHERE codigo = ?", (codigo,))
    if cliente is None:
        return redirect(url_for("clientes.clientes_lista", erro="Cliente não encontrado."))

    nomes_cliente = {str(cliente.get(k, "")).strip().casefold() for k in ("nome", "nome_fantasia", "razao_social")}

    # não exclui se algum produto, lote, movimentação ou ordem usa este cliente
    registros = consultar(
        "SELECT cliente FROM produtos UNION ALL SELECT cliente FROM lotes "
        "UNION ALL SELECT cliente FROM movimentacoes UNION ALL SELECT cliente FROM ordens")
    if any(str(r.get("cliente", "")).strip().casefold() in nomes_cliente for r in registros):
        return redirect(url_for("clientes.clientes_lista",
            erro="Não é possível excluir este cliente, pois existem registros vinculados a ele."))

    with transacao() as db:
        db.execute("DELETE FROM clientes WHERE id = ?", (cliente["id"],))
    return redirect(url_for("clientes.clientes_lista", sucesso="Cliente excluído com sucesso!"))
