<<<<<<< HEAD
# Consulta e filtragem do histórico de movimentações do estoque.
from datetime import datetime
=======
#mostra o que ja aconteceu no estoque

>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
from flask import Blueprint, render_template, request, session, redirect, url_for
from dados import movimentacoes

historico_bp = Blueprint("historico", __name__)


<<<<<<< HEAD
def _data_iso(data_texto):
    """Converte datas do histórico para YYYY-MM-DD, mantendo datas inválidas no fim."""
    if not data_texto:
        return ""
    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(str(data_texto), formato).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return ""


=======
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
@historico_bp.route("/historico")
def historico():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

<<<<<<< HEAD
    busca = request.args.get("busca", "").strip()
    tipo = request.args.get("tipo", "").strip()
    data_inicio = request.args.get("data_inicio", "").strip()
    data_fim = request.args.get("data_fim", "").strip()

    lista = []
    for m in movimentacoes:
        texto = " ".join(str(m.get(campo, "") or "") for campo in (
            "data", "produto", "tipo", "origem", "doc_origem", "fornecedor",
            "local", "doc_destino", "cliente", "usuario", "observacao"
        )).casefold()
        data_mov = _data_iso(m.get("data", ""))

        if busca and busca.casefold() not in texto:
            continue
        if tipo and m.get("tipo", "") != tipo:
            continue
        if data_inicio and (not data_mov or data_mov < data_inicio):
            continue
        if data_fim and (not data_mov or data_mov > data_fim):
            continue
        item = dict(m)
        item["data_iso"] = data_mov
        lista.append(item)

    # Ordena pela data mais recente; datas que não puderam ser interpretadas ficam no fim.
    lista.sort(key=lambda m: (bool(m.get("data_iso")), m.get("data_iso", "")), reverse=True)

    entradas_total = sum(abs(int(m.get("quantidade", 0) or 0)) for m in lista if m.get("tipo") == "Entrada")
    saidas_total = sum(abs(int(m.get("quantidade", 0) or 0)) for m in lista if m.get("tipo") == "Saída")

    return render_template(
        "historico.html",
        movimentacoes=lista,
        busca=busca,
        tipo=tipo,
        data_inicio=data_inicio,
        data_fim=data_fim,
        total_registros=len(lista),
        entradas_total=entradas_total,
        saidas_total=saidas_total,
    )
=======
    busca = request.args.get("busca", "")
    lista = []
    for m in movimentacoes:
        if busca.lower() in m["produto"].lower():
            lista.append(m)

    return render_template("historico.html", movimentacoes=lista, busca=busca)
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
