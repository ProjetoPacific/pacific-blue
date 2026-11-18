# camada do banco de dados (SQLite)
#
# Todos os dados do sistema ficam no arquivo pacific_blue.db, na mesma pasta do main.py.
# Cada alteração é gravada na hora (commit), então fechar o debug do VS Code a qualquer
# momento não perde nada. Para voltar aos dados de demonstração, apague o arquivo .db.

import os
import sqlite3
from contextlib import contextmanager

from flask import g

PASTA = os.path.dirname(os.path.abspath(__file__))
# caminho absoluto: funciona não importa de qual pasta o VS Code iniciar o programa
CAMINHO_BANCO = os.environ.get("PACIFIC_BLUE_DB", os.path.join(PASTA, "pacific_blue.db"))

VERSAO_ESQUEMA = 1

ESQUEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    senha   TEXT NOT NULL,
    nome    TEXT NOT NULL,
    email   TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS clientes (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo             TEXT NOT NULL UNIQUE COLLATE NOCASE,
    nome_fantasia      TEXT NOT NULL DEFAULT '',
    razao_social       TEXT NOT NULL DEFAULT '',
    endereco           TEXT NOT NULL DEFAULT '',
    telefone           TEXT NOT NULL DEFAULT '',
    cnpj               TEXT NOT NULL DEFAULT '',
    inscricao_estadual TEXT NOT NULL DEFAULT '',
    transferencia      TEXT NOT NULL DEFAULT '',
    data               TEXT NOT NULL DEFAULT '',
    nome               TEXT NOT NULL DEFAULT '',
    email              TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS produtos (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    referencia     TEXT NOT NULL UNIQUE COLLATE NOCASE,
    descricao      TEXT NOT NULL DEFAULT '',
    cor            TEXT NOT NULL DEFAULT '',
    tamanho        TEXT NOT NULL DEFAULT '',
    genero         TEXT NOT NULL DEFAULT '',
    grupo          TEXT NOT NULL DEFAULT '',
    grade          TEXT NOT NULL DEFAULT '',
    data           TEXT NOT NULL DEFAULT '',
    cliente        TEXT NOT NULL DEFAULT '',
    fornecedor     TEXT NOT NULL DEFAULT '',
    estoque        INTEGER NOT NULL DEFAULT 0 CHECK (estoque >= 0),
    estoque_minimo INTEGER NOT NULL DEFAULT 10
);

CREATE TABLE IF NOT EXISTS movimentacoes (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    data           TEXT NOT NULL DEFAULT '',
    produto        TEXT NOT NULL,
    tipo           TEXT NOT NULL CHECK (tipo IN ('Entrada', 'Saída')),
    origem         TEXT NOT NULL DEFAULT '',
    ordem_producao TEXT,
    doc_origem     TEXT NOT NULL DEFAULT '',
    fornecedor     TEXT NOT NULL DEFAULT '',
    quantidade     INTEGER NOT NULL,
    local          TEXT NOT NULL DEFAULT '',
    doc_destino    TEXT NOT NULL DEFAULT '',
    cliente        TEXT NOT NULL DEFAULT '',
    usuario        TEXT NOT NULL DEFAULT '',
    observacao     TEXT
);
CREATE INDEX IF NOT EXISTS idx_movimentacoes_tipo    ON movimentacoes (tipo);
CREATE INDEX IF NOT EXISTS idx_movimentacoes_produto ON movimentacoes (produto);

CREATE TABLE IF NOT EXISTS lotes (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    numero       TEXT NOT NULL UNIQUE COLLATE NOCASE,
    referencia   TEXT NOT NULL DEFAULT '',
    data_entrada TEXT NOT NULL DEFAULT '',
    cliente      TEXT NOT NULL DEFAULT '',
    status       TEXT NOT NULL DEFAULT 'Recebido'
);

CREATE TABLE IF NOT EXISTS ordens (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    numero             TEXT NOT NULL UNIQUE COLLATE NOCASE,
    cliente            TEXT NOT NULL DEFAULT '',
    referencia         TEXT NOT NULL DEFAULT '',
    local              TEXT NOT NULL DEFAULT '',
    data_chegada       TEXT NOT NULL DEFAULT '',
    ultima_atualizacao TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS ordens_processos (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    ordem_id INTEGER NOT NULL REFERENCES ordens (id) ON DELETE CASCADE,
    processo TEXT NOT NULL
);
"""


def _conectar():
    con = sqlite3.connect(CAMINHO_BANCO)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


# ---------------------------------------------------------------------------
# conexão usada durante uma requisição do Flask
# ---------------------------------------------------------------------------

def get_db():
    if "db" not in g:
        g.db = _conectar()
    return g.db


def fechar_banco(_erro=None):
    """Fecha a conexão no fim da requisição (o que não foi confirmado é desfeito)."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


@contextmanager
def transacao():
    """Agrupa várias alterações: ou grava tudo, ou não grava nada."""
    db = get_db()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise


def _como_dict(linha, sem_nulos=False):
    d = dict(linha)
    if sem_nulos:
        d = {k: v for k, v in d.items() if v is not None}
    return d


def consultar(sql, params=(), sem_nulos=False):
    """Devolve uma lista de dicionários (o mesmo formato que as telas já usavam)."""
    linhas = get_db().execute(sql, params).fetchall()
    return [_como_dict(l, sem_nulos) for l in linhas]


def consultar_um(sql, params=(), sem_nulos=False):
    linha = get_db().execute(sql, params).fetchone()
    return _como_dict(linha, sem_nulos) if linha is not None else None


# ---------------------------------------------------------------------------
# criação do banco e carga inicial
# ---------------------------------------------------------------------------

def iniciar_banco():
    """Cria o banco na primeira execução, com os dados de demonstração de dados.py.

    Nas execuções seguintes não faz nada: o que está no .db é a verdade.
    """
    con = _conectar()
    try:
        if con.execute("PRAGMA user_version").fetchone()[0] >= VERSAO_ESQUEMA:
            return
        con.executescript(ESQUEMA)
        with con:  # uma única transação: carga completa ou nada
            _carga_inicial(con)
            con.execute(f"PRAGMA user_version = {VERSAO_ESQUEMA}")
    finally:
        con.close()


def _carga_inicial(con):
    import dados

    for u in dados.usuarios:
        con.execute(
            "INSERT INTO usuarios (usuario, senha, nome, email) VALUES (?, ?, ?, ?)",
            (u["usuario"], u["senha"], u["nome"], u.get("email", "")),
        )

    colunas_cliente = ("codigo", "nome_fantasia", "razao_social", "endereco", "telefone",
                       "cnpj", "inscricao_estadual", "transferencia", "data", "nome", "email")
    for c in dados.clientes:
        con.execute(
            f"INSERT INTO clientes ({', '.join(colunas_cliente)}) "
            f"VALUES ({', '.join('?' * len(colunas_cliente))})",
            tuple(c.get(k, "") for k in colunas_cliente),
        )

    colunas_produto = ("referencia", "descricao", "cor", "tamanho", "genero", "grupo", "grade",
                       "data", "cliente", "fornecedor", "estoque", "estoque_minimo")
    for p in dados.produtos:
        con.execute(
            f"INSERT INTO produtos ({', '.join(colunas_produto)}) "
            f"VALUES ({', '.join('?' * len(colunas_produto))})",
            tuple(p.get(k, "") for k in colunas_produto),
        )

    colunas_mov = ("data", "produto", "tipo", "origem", "ordem_producao", "doc_origem", "fornecedor",
                   "quantidade", "local", "doc_destino", "cliente", "usuario", "observacao")
    for m in dados.movimentacoes:
        con.execute(
            f"INSERT INTO movimentacoes ({', '.join(colunas_mov)}) "
            f"VALUES ({', '.join('?' * len(colunas_mov))})",
            tuple(m.get(k) for k in colunas_mov),  # ausente vira NULL, como antes (chave inexistente)
        )

    for l in dados.lotes:
        con.execute(
            "INSERT INTO lotes (numero, referencia, data_entrada, cliente, status) VALUES (?, ?, ?, ?, ?)",
            (l["numero"], l["referencia"], l["data_entrada"], l["cliente"], l["status"]),
        )

    for o in dados.ordens:
        cur = con.execute(
            "INSERT INTO ordens (numero, cliente, referencia, local, data_chegada, ultima_atualizacao) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (o["numero"], o.get("cliente", ""), o.get("referencia", ""), o.get("local", ""),
             o.get("data_chegada", ""), o.get("ultima_atualizacao", "")),
        )
        con.executemany(
            "INSERT INTO ordens_processos (ordem_id, processo) VALUES (?, ?)",
            [(cur.lastrowid, p) for p in o.get("processos", [])],
        )
