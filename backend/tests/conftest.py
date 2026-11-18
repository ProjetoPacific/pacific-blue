# preparação dos testes: cada teste usa um banco temporário novo, com os dados de demonstração.
# O banco real (pacific_blue.db) nunca é tocado.

import os
import sys
import tempfile

import pytest

# permite importar main.py e banco.py, que ficam na pasta backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# precisa ser definido ANTES de importar o main, que cria o banco ao ser importado
os.environ["PACIFIC_BLUE_DB"] = os.path.join(tempfile.mkdtemp(prefix="pacific_blue_import_"), "import.db")

import banco  # noqa: E402
from main import app  # noqa: E402


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Cliente de teste ligado a um banco temporário recém-criado."""
    monkeypatch.setattr(banco, "CAMINHO_BANCO", str(tmp_path / "teste.db"))
    banco.iniciar_banco()
    app.config.update(TESTING=True)
    with app.test_client() as c:
        yield c


@pytest.fixture
def logado(client):
    """Cliente já autenticado com o usuário de demonstração caue."""
    resposta = client.post("/", data={"usuario": "caue", "senha": "1234"})
    assert resposta.status_code == 302
    return client


def consulta(sql, params=()):
    """Lê direto do banco de teste (fora de uma requisição)."""
    con = banco._conectar()
    try:
        return [dict(l) for l in con.execute(sql, params).fetchall()]
    finally:
        con.close()
