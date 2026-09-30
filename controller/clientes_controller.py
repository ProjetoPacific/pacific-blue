#cadastra e procura clientes

from flask import Blueprint, render_template, request, redirect, url_for, session
from dados import clientes

clientes_bp = Blueprint("clientes", __name__)


@clientes_bp.route("/clientes")
def clientes_lista():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    busca = request.args.get("busca", "")
    lista = []
    for c in clientes:
        texto = (c["nome"] + " " + c["telefone"] + " " + c["email"]).lower()
        if busca.lower() in texto:
            lista.append(c)

    return render_template("clientes.html", clientes=lista, busca=busca)


@clientes_bp.route("/clientes/novo", methods=["GET", "POST"])
def novo_cliente():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    erro = None
    if request.method == "POST":
        nome = request.form.get("nome").strip()
        telefone = request.form.get("telefone").strip()
        email = request.form.get("email").strip()

        existe = False
        for c in clientes:
            if c["nome"].lower() == nome.lower():
                existe = True

        if existe:
            erro = "Esse cliente já está cadastrado."
        else:
            clientes.append({"nome": nome, "telefone": telefone, "email": email})
            return redirect(url_for("clientes.clientes_lista"))

    return render_template("novo_cliente.html", erro=erro)
