from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect, url_for, session
from banco import consultar, consultar_um, transacao

ordens_bp = Blueprint("ordens", __name__)

PROCESSOS = [
    "used",
    "laser",
    "destroyed",
    "stone",
    "marmorizado",
    "tingimento",
    "amaciado",
]


def hoje_iso():
    return date.today().isoformat()


def formatar_data(valor):
    if not valor:
        return "-"
    try:
        return datetime.strptime(valor, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return valor


def carregar_ordens(numero=None):
    """Lê as ordens do banco, cada uma com a lista de processos (mesmo formato de antes)."""
    sql = "SELECT * FROM ordens"
    params = ()
    if numero is not None:
        sql += " WHERE numero = ?"
        params = (numero,)
    ordens = consultar(sql + " ORDER BY id", params)
    por_id = {o["id"]: o for o in ordens}
    for o in ordens:
        o["processos"] = []
    for p in consultar("SELECT ordem_id, processo FROM ordens_processos ORDER BY id"):
        if p["ordem_id"] in por_id:
            por_id[p["ordem_id"]]["processos"].append(p["processo"])
    return ordens


def salvar_processos(db, ordem_id, processos):
    db.execute("DELETE FROM ordens_processos WHERE ordem_id = ?", (ordem_id,))
    db.executemany("INSERT INTO ordens_processos (ordem_id, processo) VALUES (?, ?)",
                   [(ordem_id, p) for p in processos])


def nomes_clientes():
    return [c.get("nome", "") for c in consultar("SELECT nome FROM clientes ORDER BY id")]


def preparar_ordem(ordem):
    try:
        ultima = date.fromisoformat(ordem.get("ultima_atualizacao", hoje_iso()))
        ordem["dias_atualizacao"] = max(0, (date.today() - ultima).days)
    except (TypeError, ValueError):
        ordem["dias_atualizacao"] = 0
    ordem["chegada_formatada"] = formatar_data(ordem.get("data_chegada"))
    ordem["ultima_atualizacao_formatada"] = formatar_data(ordem.get("ultima_atualizacao"))
    return ordem


@ordens_bp.route("/ordens")
def ordens_lista():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    busca = request.args.get("busca", "").strip().lower()
    lista = []
    for ordem in carregar_ordens():
        texto = " ".join([
            str(ordem.get("numero", "")),
            str(ordem.get("cliente", "")),
            str(ordem.get("referencia", "")),
            str(ordem.get("local", "")),
            " ".join(ordem.get("processos", [])),
        ]).lower()
        if busca in texto:
            lista.append(preparar_ordem(ordem))

    return render_template("ordens.html", ordens=lista, busca=busca)


@ordens_bp.route("/ordens/nova", methods=["GET", "POST"])
def nova_ordem():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    erro = None
    if request.method == "POST":
        numero = request.form.get("numero", "").strip()
        cliente = request.form.get("cliente", "").strip()
        referencia = request.form.get("referencia", "").strip()
        local = request.form.get("local", "").strip()
        data_chegada = request.form.get("data_chegada", "").strip()
        processos_selecionados = [p for p in PROCESSOS if p in request.form.getlist("processos")]

        if not all([numero, cliente, referencia, local, data_chegada]):
            erro = "Preencha todos os campos obrigatórios."
        elif consultar_um("SELECT 1 FROM ordens WHERE numero = ?", (numero,)):
            erro = "Esse código de ordem já está cadastrado."
        else:
            with transacao() as db:
                nova = db.execute(
                    "INSERT INTO ordens (numero, cliente, referencia, local, data_chegada, ultima_atualizacao) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (numero, cliente, referencia, local, data_chegada, hoje_iso()))
                salvar_processos(db, nova.lastrowid, processos_selecionados)
            return redirect(url_for("ordens.ordens_lista"))

    return render_template(
        "nova_ordem.html",
        ordem=None,
        clientes=nomes_clientes(),
        processos=PROCESSOS,
        erro=erro,
        hoje=hoje_iso(),
    )


@ordens_bp.route("/ordens/<numero>/editar", methods=["GET", "POST"])
def editar_ordem(numero):
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    encontradas = carregar_ordens(numero)
    ordem = encontradas[0] if encontradas else None
    if ordem is None:
        return redirect(url_for("ordens.ordens_lista"))

    erro = None
    if request.method == "POST":
        cliente = request.form.get("cliente", "").strip()
        referencia = request.form.get("referencia", "").strip()
        local = request.form.get("local", "").strip()
        data_chegada = request.form.get("data_chegada", "").strip()
        processos_selecionados = [p for p in PROCESSOS if p in request.form.getlist("processos")]

        if not all([cliente, referencia, local, data_chegada]):
            erro = "Preencha todos os campos obrigatórios."
        else:
            with transacao() as db:
                db.execute(
                    "UPDATE ordens SET cliente = ?, referencia = ?, local = ?, data_chegada = ?, "
                    "ultima_atualizacao = ? WHERE id = ?",
                    (cliente, referencia, local, data_chegada, hoje_iso(), ordem["id"]))
                salvar_processos(db, ordem["id"], processos_selecionados)
            return redirect(url_for("ordens.ordens_lista"))

    return render_template(
        "nova_ordem.html",
        ordem=ordem,
        clientes=nomes_clientes(),
        processos=PROCESSOS,
        erro=erro,
        hoje=hoje_iso(),
    )


@ordens_bp.route("/ordens/<numero>/excluir", methods=["POST"])
def excluir_ordem(numero):
    if "usuario" not in session:
        return redirect(url_for("login.login"))
    with transacao() as db:
        db.execute("DELETE FROM ordens WHERE numero = ?", (numero,))  # os processos saem junto (CASCADE)
    return redirect(url_for("ordens.ordens_lista"))
