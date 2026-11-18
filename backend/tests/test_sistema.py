import sqlite3

import pytest

import banco
from conftest import consulta


def texto(resposta):
    return resposta.get_data(as_text=True)


def estoque_de(referencia):
    return consulta("SELECT estoque FROM produtos WHERE referencia = ?", (referencia,))[0]["estoque"]


# ---------------------------------------------------------------- acesso

ROTAS_PROTEGIDAS = [
    "/dashboard", "/produtos", "/produtos/novo", "/movimentacao", "/entradas", "/saidas",
    "/historico", "/clientes", "/lotes", "/usuarios", "/ordens", "/tecnologias", "/alterar-senha",
]


@pytest.mark.parametrize("rota", ROTAS_PROTEGIDAS)
def test_telas_exigem_login(client, rota):
    resposta = client.get(rota)
    assert resposta.status_code == 302
    assert resposta.headers["Location"].endswith("/")


def test_login_com_senha_errada_mostra_erro(client):
    resposta = client.post("/", data={"usuario": "caue", "senha": "errada"})
    assert resposta.status_code == 200
    assert "Usuário ou senha inválidos" in texto(resposta)


def test_login_correto_leva_ao_dashboard(client):
    resposta = client.post("/", data={"usuario": "caue", "senha": "1234"})
    assert resposta.status_code == 302
    assert resposta.headers["Location"].endswith("/dashboard")


def test_sair_encerra_a_sessao(logado):
    assert logado.get("/dashboard").status_code == 200
    logado.get("/sair")
    assert logado.get("/dashboard").status_code == 302


def test_cadastro_de_usuario_novo_e_duplicado(client):
    dados = {"nome": "Teste", "email": "t@t.com", "usuario": "teste", "senha": "abc", "confirmar": "abc"}
    assert "Conta criada com sucesso" in texto(client.post("/cadastro", data=dados))
    assert "Esse usuário já existe" in texto(client.post("/cadastro", data=dados))


# ---------------------------------------------------------------- dashboard

def test_dashboard_mostra_dados_de_demonstracao(logado):
    html = texto(logado.get("/dashboard"))
    assert "621" in html  # total de peças dos dados de demonstração
    assert "PB-032" in html and "PB-045" in html  # alertas de estoque baixo


# ---------------------------------------------------------------- produtos

DADOS_PRODUTO = {"descricao": "Produto de teste", "cor": "Azul", "tamanho": "M", "genero": "Unissex",
                 "grupo": "Camisetas", "grade": "M", "data": "01/01/2026", "cliente": "PB",
                 "fornecedor": "Fornecedor 1"}


def test_cadastrar_produto_e_barrar_referencia_duplicada(logado):
    novo = dict(DADOS_PRODUTO, referencia="DEMO-1", estoque="30")
    assert logado.post("/produtos/novo", data=novo).status_code == 302
    assert estoque_de("DEMO-1") == 30

    repetido = logado.post("/produtos/novo", data=novo)
    assert "Essa referência já está cadastrada" in texto(repetido)
    assert len(consulta("SELECT 1 FROM produtos WHERE referencia = 'DEMO-1'")) == 1


def test_nao_exclui_produto_com_movimentacoes(logado):
    resposta = logado.post("/produtos/DB-001/excluir")
    assert "erro=" in resposta.headers["Location"]
    assert len(consulta("SELECT 1 FROM produtos WHERE referencia = 'DB-001'")) == 1


def test_exclui_produto_sem_vinculos(logado):
    logado.post("/produtos/novo", data=dict(DADOS_PRODUTO, referencia="DEMO-2", estoque="5"))
    resposta = logado.post("/produtos/DEMO-2/excluir")
    assert "sucesso=" in resposta.headers["Location"]
    assert consulta("SELECT 1 FROM produtos WHERE referencia = 'DEMO-2'") == []


def test_ajuste_de_saldo_gera_movimentacao(logado):
    antes = estoque_de("DB-002")
    editado = dict(DADOS_PRODUTO, referencia="DB-002", estoque=str(antes - 10))
    assert logado.post("/produtos/DB-002/editar", data=editado).status_code == 302

    assert estoque_de("DB-002") == antes - 10
    ajuste = consulta("SELECT * FROM movimentacoes WHERE produto = 'DB-002' AND origem = 'Ajuste'")
    assert len(ajuste) == 1
    assert ajuste[0]["quantidade"] == -10 and ajuste[0]["tipo"] == "Saída"


# ---------------------------------------------------------------- movimentação

def movimentar(client, tipo, quantidade, produto="DB-001"):
    return client.post("/movimentacao", data={
        "tipo": tipo, "produto": produto, "quantidade": str(quantidade), "data": "17/11/2026",
        "origem": tipo, "local": "laser", "ordem_producao": "OP-TESTE", "cliente": "DKS",
    })


def test_saida_valida_baixa_o_estoque_e_registra_o_usuario(logado):
    assert estoque_de("DB-001") == 248
    assert movimentar(logado, "Saída", 20).status_code == 302

    assert estoque_de("DB-001") == 228
    ultima = consulta("SELECT * FROM movimentacoes ORDER BY id DESC LIMIT 1")[0]
    assert ultima["produto"] == "DB-001" and ultima["quantidade"] == -20
    assert ultima["usuario"] == "Cauê Buzolin"


def test_saida_maior_que_o_saldo_e_barrada(logado):
    movimentacoes_antes = len(consulta("SELECT 1 FROM movimentacoes"))
    resposta = movimentar(logado, "Saída", 9999)

    assert "maior que o estoque disponível" in texto(resposta)
    assert estoque_de("DB-001") == 248
    assert len(consulta("SELECT 1 FROM movimentacoes")) == movimentacoes_antes


def test_entrada_aumenta_o_estoque(logado):
    assert movimentar(logado, "Entrada", 50).status_code == 302
    assert estoque_de("DB-001") == 298


def test_quantidade_zero_e_ordem_em_branco_sao_barradas(logado):
    assert "maior que zero" in texto(movimentar(logado, "Entrada", 0))

    sem_ordem = logado.post("/movimentacao", data={
        "tipo": "Entrada", "produto": "DB-001", "quantidade": "5", "origem": "Entrada",
        "local": "laser", "ordem_producao": "", "cliente": "DKS"})
    assert "Informe a ordem de produção" in texto(sem_ordem)
    assert estoque_de("DB-001") == 248


# ---------------------------------------------------------------- clientes e lotes

def test_nao_exclui_cliente_com_vinculos(logado):
    resposta = logado.post("/clientes/CLI-001/excluir")
    assert "erro=" in resposta.headers["Location"]
    assert len(consulta("SELECT 1 FROM clientes WHERE codigo = 'CLI-001'")) == 1


def test_cliente_sem_vinculos_pode_ser_excluido(logado):
    novo = {"codigo": "CLI-DEMO", "nome_fantasia": "Demo", "razao_social": "Demo Ltda."}
    assert logado.post("/clientes/novo", data=novo).status_code == 302
    resposta = logado.post("/clientes/CLI-DEMO/excluir")
    assert "sucesso=" in resposta.headers["Location"]


def test_lote_so_e_excluido_quando_concluido(logado):
    logado.post("/produtos/novo", data=dict(DADOS_PRODUTO, referencia="DEMO-3", estoque="1"))
    lote = {"referencia": "DEMO-3", "data_entrada": "17/11/2026", "cliente": "PB", "status": "Recebido"}
    assert logado.post("/lotes/novo", data=lote).status_code == 302

    # um segundo lote para a mesma referência é barrado
    assert "Já existe um lote" in texto(logado.post("/lotes/novo", data=lote))

    # em andamento: a exclusão é bloqueada
    assert "erro=" in logado.post("/lotes/DEMO-3/excluir").headers["Location"]
    assert len(consulta("SELECT 1 FROM lotes WHERE numero = 'DEMO-3'")) == 1

    # concluído: a exclusão funciona
    logado.post("/lotes/DEMO-3/editar", data=dict(lote, status="Concluído"))
    assert "sucesso=" in logado.post("/lotes/DEMO-3/excluir").headers["Location"]
    assert consulta("SELECT 1 FROM lotes WHERE numero = 'DEMO-3'") == []


# ---------------------------------------------------------------- banco de dados

def test_banco_nao_aceita_estoque_negativo():
    con = banco._conectar()
    try:
        with pytest.raises(sqlite3.IntegrityError):
            con.execute("UPDATE produtos SET estoque = -1 WHERE referencia = 'DB-001'")
    finally:
        con.close()


def test_excluir_ordem_apaga_os_processos_em_cascata(client):
    con = banco._conectar()
    try:
        ordem_id = con.execute("INSERT INTO ordens (numero) VALUES ('OP-CASCATA')").lastrowid
        con.executemany("INSERT INTO ordens_processos (ordem_id, processo) VALUES (?, ?)",
                        [(ordem_id, "Destroyed"), (ordem_id, "Bigode laser")])
        con.commit()
        assert con.execute("SELECT COUNT(*) FROM ordens_processos WHERE ordem_id = ?", (ordem_id,)).fetchone()[0] == 2

        con.execute("DELETE FROM ordens WHERE id = ?", (ordem_id,))
        con.commit()
        assert con.execute("SELECT COUNT(*) FROM ordens_processos WHERE ordem_id = ?", (ordem_id,)).fetchone()[0] == 0
    finally:
        con.close()


def test_dados_persistem_ao_reiniciar_o_banco(logado):
    movimentar(logado, "Saída", 20)
    assert estoque_de("DB-001") == 228

    # reabrir o sistema não pode voltar aos dados de demonstração
    banco.iniciar_banco()
    assert estoque_de("DB-001") == 228
