<<<<<<< HEAD
# cria ordens e muda elas de lugar
=======
#cria ordens e muda elas de lugar
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

from flask import Blueprint, render_template, request, redirect, url_for, session
from dados import ordens, produtos, clientes, locais, processos
from datas import dias_desde

ordens_bp = Blueprint("ordens", __name__)


@ordens_bp.route("/ordens")
def ordens_lista():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    busca = request.args.get("busca", "")
    lista = []
    for o in ordens:
        texto = (o["numero"] + " " + o["referencia"] + " " + o["cliente"] + " " + o["processo"] + " " + o["local"]).lower()
        if busca.lower() in texto:
            o["dias_local"] = dias_desde(o["data_local"])
            lista.append(o)

    return render_template("ordens.html", ordens=lista, busca=busca)


@ordens_bp.route("/ordens/nova", methods=["GET", "POST"])
def nova_ordem():
    if "usuario" not in session:
        return redirect(url_for("login.login"))

<<<<<<< HEAD
    erro = None

    if request.method == "POST":
        numero = request.form.get("numero").strip()
        quantidade_texto = request.form.get("quantidade")

        existe = False
        for o in ordens:
            if o["numero"].lower() == numero.lower():
                existe = True

        try:
            quantidade = int(quantidade_texto)
        except (TypeError, ValueError):
            quantidade = 0
            erro = "Digite uma quantidade válida."

        if erro is None and quantidade <= 0:
            erro = "A quantidade deve ser maior que zero."
        elif existe:
            erro = "Esse código de ordem já está cadastrado."

        if erro is None:
            referencia = request.form.get("referencia")
            cliente = request.form.get("cliente")
            processo = request.form.get("processo")
            local = request.form.get("local")
            data_local = request.form.get("data_local")
            destino = request.form.get("destino")

            ordem = {
                "numero": numero,
                "referencia": referencia,
                "cliente": cliente,
                "quantidade": quantidade,
                "processo": processo,
                "local": local,
                "data_local": data_local,
                "status": "Finalizada" if local == "Saída" else "Em produção",
                "destino": destino,
                "fluxo": [{"local": local, "data": data_local}],
            }

            if cliente == "":
                for p in produtos:
                    if p["referencia"] == referencia:
                        ordem["cliente"] = p["cliente"]

            ordens.append(ordem)
            return redirect(url_for("ordens.ordens_lista"))
=======
    if request.method == "POST":
        referencia = request.form.get("referencia")
        produto_encontrado = None
        for p in produtos:
            if p["referencia"] == referencia:
                produto_encontrado = p

        numero = request.form.get("numero")
        cliente = request.form.get("cliente")
        quantidade = int(request.form.get("quantidade"))
        processo = request.form.get("processo")
        local = request.form.get("local")
        data_local = request.form.get("data_local")
        destino = request.form.get("destino")

        ordem = {
            "numero": numero,
            "referencia": referencia,
            "cliente": cliente,
            "quantidade": quantidade,
            "processo": processo,
            "local": local,
            "data_local": data_local,
            "status": "Finalizada" if local == "Saída" else "Em produção",
            "destino": destino,
            "fluxo": [{"local": local, "data": data_local}],
        }
        if produto_encontrado is not None and cliente == "":
            ordem["cliente"] = produto_encontrado["cliente"]
        ordens.append(ordem)
        return redirect(url_for("ordens.ordens_lista"))
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

    referencias = []
    for p in produtos:
        referencias.append(p["referencia"])
<<<<<<< HEAD

=======
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
    nomes_clientes = []
    for c in clientes:
        nomes_clientes.append(c["nome"])

<<<<<<< HEAD
    return render_template(
        "nova_ordem.html",
        referencias=referencias,
        clientes=nomes_clientes,
        locais=locais,
        processos=processos,
        erro=erro,
    )
=======
    return render_template("nova_ordem.html", referencias=referencias, clientes=nomes_clientes, locais=locais, processos=processos)
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861


@ordens_bp.route("/ordens/<numero>/mover", methods=["GET", "POST"])
def mover_ordem(numero):
    if "usuario" not in session:
        return redirect(url_for("login.login"))

    ordem = None
    for o in ordens:
        if o["numero"] == numero:
            ordem = o

    if ordem is None:
        return redirect(url_for("ordens.ordens_lista"))

    erro = None
    if request.method == "POST":
        novo_local = request.form.get("local")
        nova_data = request.form.get("data_local")
        novo_destino = request.form.get("destino", "")

        if novo_local == "":
            erro = "Selecione um local."
        elif nova_data == "":
            erro = "Informe a data da mudança."
        else:
            ordem["local"] = novo_local
            ordem["data_local"] = nova_data
            ordem["destino"] = novo_destino
            ordem["status"] = "Finalizada" if novo_local == "Saída" else "Em produção"
<<<<<<< HEAD

            local_fluxo = novo_local
            if novo_local == "Saída" and novo_destino:
                local_fluxo = "Saída para " + novo_destino

=======
            local_fluxo = novo_local
            if novo_local == "Saída" and novo_destino:
                local_fluxo = "Saída para " + novo_destino
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
            ordem["fluxo"].append({"local": local_fluxo, "data": nova_data})
            return redirect(url_for("ordens.ordens_lista"))

    return render_template("mover_ordem.html", ordem=ordem, locais=locais, erro=erro)
