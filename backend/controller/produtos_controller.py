from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, session
from dados import fornecedores, grupos, generos
from banco import consultar, consultar_um, transacao

produtos_bp = Blueprint("produtos", __name__)

def nomes_clientes():
    return [c.get("nome_fantasia") or c.get("nome", "")
            for c in consultar("SELECT nome_fantasia, nome FROM clientes ORDER BY id")]

def campos_do_form():
    """Campos de texto do formulário de produto (sem referência e estoque)."""
    return (request.form.get("descricao","").strip(), request.form.get("cor","").strip(),
            request.form.get("tamanho","").strip(), request.form.get("genero",""),
            request.form.get("grupo",""), request.form.get("grade","").strip(),
            request.form.get("data","").strip(), request.form.get("cliente",""),
            request.form.get("fornecedor",""))

@produtos_bp.route("/produtos")
def produtos_lista():
    if "usuario" not in session:
        return redirect(url_for("login.login"))
    busca = request.args.get("busca", "")
    grupo = request.args.get("grupo", "Todos")
    cliente = request.args.get("cliente", "Todos")
    lista = []
    for prod in consultar("SELECT * FROM produtos ORDER BY id"):
        texto = " ".join(str(prod.get(k, "")) for k in
            ("referencia","descricao","cor","tamanho","genero","grupo","grade","cliente","fornecedor")).lower()
        if busca.lower() not in texto: continue
        if grupo != "Todos" and prod.get("grupo") != grupo: continue
        if cliente != "Todos" and prod.get("cliente") != cliente: continue
        lista.append(prod)
    return render_template("produtos.html", produtos=lista, busca=busca, grupo=grupo,
        cliente=cliente, grupos=grupos, clientes=nomes_clientes(), erro=request.args.get("erro"), sucesso=request.args.get("sucesso"))

def formulario_produto(produto=None, erro=None):
    return render_template("cadastrar_produto.html", produto=produto, grupos=grupos,
        generos=generos, clientes=nomes_clientes(), fornecedores=fornecedores, erro=erro)

@produtos_bp.route("/produtos/novo", methods=["GET", "POST"])
def novo_produto():
    if "usuario" not in session: return redirect(url_for("login.login"))
    erro = None
    if request.method == "POST":
        referencia = request.form.get("referencia", "").strip()
        if not referencia:
            erro = "Informe a referência."
        elif consultar_um("SELECT 1 FROM produtos WHERE referencia = ?", (referencia,)):
            erro = "Essa referência já está cadastrada."
        else:
            try: estoque = max(0, int(request.form.get("estoque", "0")))
            except ValueError: estoque = 0
            with transacao() as db:
                db.execute(
                    "INSERT INTO produtos (referencia, descricao, cor, tamanho, genero, grupo, grade, data, "
                    "cliente, fornecedor, estoque, estoque_minimo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 10)",
                    (referencia,) + campos_do_form() + (estoque,))
            return redirect(url_for("produtos.produtos_lista"))
    return formulario_produto(erro=erro)

@produtos_bp.route("/produtos/<referencia>/editar", methods=["GET", "POST"])
def editar_produto(referencia):
    if "usuario" not in session: return redirect(url_for("login.login"))
    produto = consultar_um("SELECT * FROM produtos WHERE referencia = ?", (referencia,))
    if produto is None: return redirect(url_for("produtos.produtos_lista"))
    erro = None
    if request.method == "POST":
        nova_ref = request.form.get("referencia", "").strip()
        referencia_antiga = produto["referencia"]
        if not nova_ref: erro = "Informe a referência."
        elif consultar_um("SELECT 1 FROM produtos WHERE referencia = ? AND id <> ?", (nova_ref, produto["id"])):
            erro = "Essa referência já está cadastrada."
        elif nova_ref != referencia_antiga and consultar_um(
                "SELECT 1 FROM lotes WHERE numero = ? AND numero <> ?", (nova_ref, referencia_antiga)):
            erro = "Já existe um lote com a referência informada; não é possível renomear o produto para ela."
        else:
            try: estoque = int(request.form.get("estoque", "0"))
            except ValueError: estoque = -1
            if estoque < 0: erro = "A quantidade em estoque deve ser um número igual ou maior que zero."
            else:
                saldo_anterior = int(produto.get("estoque", 0) or 0)
                diferenca = estoque - saldo_anterior
                # tudo numa transação só: produto, referências ligadas e ajuste de saldo
                with transacao() as db:
                    db.execute(
                        "UPDATE produtos SET referencia = ?, descricao = ?, cor = ?, tamanho = ?, genero = ?, "
                        "grupo = ?, grade = ?, data = ?, cliente = ?, fornecedor = ?, estoque = ? WHERE id = ?",
                        (nova_ref,) + campos_do_form() + (estoque, produto["id"]))
                    if referencia_antiga != nova_ref:
                        db.execute("UPDATE movimentacoes SET produto = ? WHERE produto = ?", (nova_ref, referencia_antiga))
                        db.execute("UPDATE lotes SET numero = ? WHERE numero = ?", (nova_ref, referencia_antiga))
                        db.execute("UPDATE lotes SET referencia = ? WHERE referencia = ?", (nova_ref, referencia_antiga))
                        db.execute("UPDATE ordens SET referencia = ? WHERE referencia = ?", (nova_ref, referencia_antiga))
                    if diferenca:
                        db.execute(
                            "INSERT INTO movimentacoes (data, produto, tipo, origem, doc_origem, fornecedor, quantidade, "
                            "local, doc_destino, cliente, usuario, observacao) "
                            "VALUES (?, ?, ?, 'Ajuste', '', '', ?, '', '', '', ?, ?)",
                            (date.today().strftime("%d/%m/%Y"), nova_ref, "Entrada" if diferenca > 0 else "Saída",
                             diferenca, session["usuario"], "Ajuste manual do saldo pela edição do produto."))
                return redirect(url_for("produtos.produtos_lista"))
    return formulario_produto(produto, erro)

@produtos_bp.route("/produtos/<referencia>/excluir", methods=["POST"])
def excluir_produto(referencia):
    if "usuario" not in session: return redirect(url_for("login.login"))
    produto = consultar_um("SELECT id, referencia FROM produtos WHERE referencia = ?", (referencia,))
    if produto is None:
        return redirect(url_for("produtos.produtos_lista", erro="Produto não encontrado."))

    ref = produto["referencia"]
    # não exclui se houver movimentação, lote ou ordem usando este produto
    vinculado = consultar_um(
        "SELECT EXISTS (SELECT 1 FROM movimentacoes WHERE produto = ?) "
        "OR EXISTS (SELECT 1 FROM lotes WHERE referencia = ? OR numero = ?) "
        "OR EXISTS (SELECT 1 FROM ordens WHERE referencia = ?) AS vinculado",
        (ref, ref, ref, ref))["vinculado"]
    if vinculado:
        return redirect(url_for("produtos.produtos_lista",
            erro="Não é possível excluir: existem registros vinculados a este produto."))

    with transacao() as db:
        db.execute("DELETE FROM produtos WHERE id = ?", (produto["id"],))
    return redirect(url_for("produtos.produtos_lista", sucesso="Produto excluído com sucesso!"))
