# cria e procura lotes

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
        texto = (l["numero"] + " " + l["cliente"] + " " + l["status"]).lower()
        if busca.lower() in texto:
            lista.append(l)

    return render_template("lotes.html", lotes=lista, busca=busca)


@lotes_bp.route("/lotes/novo", methods=["GET", "POST"])
def novo_lote():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

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
