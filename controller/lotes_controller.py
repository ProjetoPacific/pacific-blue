<<<<<<< HEAD
# cria e procura lotes
=======
#cria, procura e converte lotes
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

from flask import Blueprint, render_template, request, redirect, url_for, session
from dados import lotes

lotes_bp = Blueprint("lotes", __name__)


@lotes_bp.route("/lotes")
def lotes_lista():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    busca = request.args.get("busca", "")
    lista = []
    for l in lotes:
<<<<<<< HEAD
        texto = (l["numero"] + " " + l["cliente"] + " " + l["status"]).lower()
        if busca.lower() in texto:
=======
        if busca.lower() in l["numero"].lower() or busca.lower() in l["cliente"].lower():
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
            lista.append(l)

    return render_template("lotes.html", lotes=lista, busca=busca)


@lotes_bp.route("/lotes/novo", methods=["GET", "POST"])
def novo_lote():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

<<<<<<< HEAD
    erro = None

    if request.method == "POST":
        numero = request.form.get("numero").strip()

        existe = False
        for l in lotes:
            if l["numero"].lower() == numero.lower():
                existe = True

        if existe:
            erro = "Esse lote já está cadastrado."
        else:
            lotes.append({
                "numero": numero,
                "data_entrada": request.form.get("data_entrada").strip(),
                "cliente": request.form.get("cliente").strip(),
                "status": "Recebido",
            })
            return redirect(url_for("lotes.lotes_lista"))

    return render_template("novo_lote.html", erro=erro)
=======
    if request.method == "POST":
        lote = {
            "numero": request.form.get("numero"),
            "data_entrada": request.form.get("data_entrada"),
            "cliente": request.form.get("cliente"),
            "status": "Recebido",
        }
        lotes.append(lote)
        return redirect(url_for("lotes.lotes_lista"))

    return render_template("novo_lote.html")


@lotes_bp.route("/lotes/<numero>/conversao", methods=["GET", "POST"])
def conversao_lote(numero):
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    lote = None
    for l in lotes:
        if l["numero"] == numero:
            lote = l

    tamanhos = ["36", "38", "40", "42", "44", "46", "48"]

    if request.method == "POST":
        for l in lotes:
            if l["numero"] == numero:
                l["status"] = "Recebido"
        return redirect(url_for("lotes.lotes_lista"))

    return render_template("conversao_lote.html", lote=lote, tamanhos=tamanhos)
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
