from flask import Blueprint, render_template, request, redirect, url_for, session
from banco import consultar, consultar_um, transacao

lotes_bp = Blueprint("lotes", __name__)

def lista_produtos():
    return consultar("SELECT referencia, descricao FROM produtos ORDER BY id")

def dados_form(produto):
    return (produto["referencia"], produto["referencia"],
            request.form.get("data_entrada","").strip(),
            request.form.get("cliente","").strip(), request.form.get("status","Recebido"))

@lotes_bp.route("/lotes")
def lotes_lista():
    if "usuario" not in session: return redirect(url_for("login.login"))
    busca = request.args.get("busca", "").casefold()
    todos = consultar("SELECT numero, referencia, data_entrada, cliente, status FROM lotes ORDER BY id")
    lista = [l for l in todos if busca in " ".join(str(l.get(k,"")) for k in ("numero","cliente","status")).casefold()]
    return render_template("lotes.html", lotes=lista, busca=busca, erro=request.args.get("erro"), sucesso=request.args.get("sucesso"))

@lotes_bp.route("/lotes/novo", methods=["GET","POST"])
def novo_lote():
    if "usuario" not in session: return redirect(url_for("login.login"))
    erro = None
    if request.method == "POST":
        referencia = request.form.get("referencia","").strip()
        produto = consultar_um("SELECT referencia FROM produtos WHERE referencia = ?", (referencia,))
        if not produto: erro = "Selecione uma referência de produto válida."
        elif consultar_um("SELECT 1 FROM lotes WHERE numero = ?", (referencia,)):
            erro = "Já existe um lote para essa referência. Edite o lote existente."
        else:
            with transacao() as db:
                db.execute("INSERT INTO lotes (numero, referencia, data_entrada, cliente, status) VALUES (?, ?, ?, ?, ?)",
                           dados_form(produto))
            return redirect(url_for("lotes.lotes_lista"))
    return render_template("novo_lote.html", lote=None, produtos=lista_produtos(), erro=erro)

@lotes_bp.route("/lotes/<numero>/editar", methods=["GET","POST"])
def editar_lote(numero):
    if "usuario" not in session: return redirect(url_for("login.login"))
    lote = consultar_um("SELECT id, numero, referencia, data_entrada, cliente, status FROM lotes WHERE numero = ?", (numero,))
    if lote is None: return redirect(url_for("lotes.lotes_lista"))
    erro = None
    if request.method == "POST":
        referencia = request.form.get("referencia","").strip()
        produto = consultar_um("SELECT referencia FROM produtos WHERE referencia = ?", (referencia,))
        if not produto: erro = "Selecione uma referência de produto válida."
        elif consultar_um("SELECT 1 FROM lotes WHERE numero = ? AND id <> ?", (referencia, lote["id"])):
            erro = "Já existe um lote com essa referência."
        else:
            with transacao() as db:
                db.execute("UPDATE lotes SET numero = ?, referencia = ?, data_entrada = ?, cliente = ?, status = ? WHERE id = ?",
                           dados_form(produto) + (lote["id"],))
            return redirect(url_for("lotes.lotes_lista"))
    return render_template("novo_lote.html", lote=lote, produtos=lista_produtos(), erro=erro)

@lotes_bp.route("/lotes/<numero>/excluir", methods=["POST"])
def excluir_lote(numero):
    if "usuario" not in session: return redirect(url_for("login.login"))
    lote = consultar_um("SELECT id, status FROM lotes WHERE numero = ?", (numero,))
    if lote is None:
        return redirect(url_for("lotes.lotes_lista", erro="Lote não encontrado."))

    # só permite excluir lotes concluídos
    if str(lote["status"]).strip().casefold() not in ["concluído", "concluido"]:
        return redirect(url_for("lotes.lotes_lista",
            erro="Não é possível excluir. O lote precisa estar com status Concluído."))

    with transacao() as db:
        db.execute("DELETE FROM lotes WHERE id = ?", (lote["id"],))
    return redirect(url_for("lotes.lotes_lista", sucesso="Lote concluído excluído com sucesso!"))
