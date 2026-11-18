# dados de demonstração e opções fixas dos formulários
#
# ATENÇÃO: as listas usuarios, clientes, produtos, movimentacoes, lotes e ordens só são
# usadas UMA vez, para criar o banco (pacific_blue.db) na primeira execução.
# Depois disso os dados vivem no banco; mudar essas listas não altera o que já foi criado.
# As listas fornecedores, grupos, generos, locais etc. continuam sendo usadas direto pelas telas.

usuarios = [
    {"usuario": "caue", "senha": "1234", "nome": "Cauê Buzolin", "email": "caue@email.com"},
    {"usuario": "kauan", "senha": "1234", "nome": "Kauan Constancio", "email": "kauan@email.com"},
    {"usuario": "gabriel", "senha": "1234", "nome": "Gabriel Guerra", "email": "gabriel@email.com"},
    {"usuario": "kaue", "senha": "1234", "nome": "Kaue Giovani", "email": "kaue@email.com"},
    {"usuario": "mahmoud", "senha": "1234", "nome": "Mahmoud Rkaine", "email": "mahmoud@email.com"},
]

clientes = [
    {"codigo":"CLI-001","nome_fantasia":"DKS","razao_social":"DKS Confecções Ltda.","endereco":"","telefone":"-","cnpj":"","inscricao_estadual":"","transferencia":"","data":"","nome":"DKS","email":""},
    {"codigo":"CLI-002","nome_fantasia":"PB","razao_social":"Pacific Blue","endereco":"","telefone":"-","cnpj":"","inscricao_estadual":"","transferencia":"","data":"","nome":"PB","email":""},
    {"codigo":"CLI-003","nome_fantasia":"AC","razao_social":"AC Confecções","endereco":"","telefone":"-","cnpj":"","inscricao_estadual":"","transferencia":"","data":"","nome":"AC","email":""},
]

# Opções usadas nos campos de seleção.
fornecedores = ["Fornecedor 1", "Fornecedor 2", "Fornecedor 3"]

# Opções de origem para cada tipo de movimentação.
origens_movimentacao = {
    "Entrada": ["Compra", "Ajuste", "Devolução"],
    "Saída": ["Venda", "Ajuste"],
}
grupos = ["Calças", "Camisetas", "Jaquetas", "Bermudas"]
generos = ["Masculino", "Feminino", "Unissex"]
locais = ["used", "laser", "destroyed", "stone", "marmorizado", "tingimento", "amaciado", "parado"]
processos = ["Destroyed", "Used local", "Bigode laser"]

produtos = [
    {
        "referencia": "DB-001", "descricao": "Calça jeans reta", "cor": "Azul", "tamanho": "36 a 48",
        "genero": "Masculino", "grupo": "Calças", "grade": "36 a 48", "data": "16/09/2026",
        "cliente": "DKS", "fornecedor": "Fornecedor 1", "estoque": 248, "estoque_minimo": 10
    },
    {
        "referencia": "DB-002", "descricao": "Calça jeans skinny", "cor": "Azul", "tamanho": "36 a 46",
        "genero": "Feminino", "grupo": "Calças", "grade": "36 a 46", "data": "15/09/2026",
        "cliente": "DKS", "fornecedor": "Fornecedor 1", "estoque": 180, "estoque_minimo": 15
    },
    {
        "referencia": "PB-032", "descricao": "Camiseta básica", "cor": "Branca", "tamanho": "P a GG",
        "genero": "Unissex", "grupo": "Camisetas", "grade": "P a GG", "data": "16/09/2026",
        "cliente": "PB", "fornecedor": "Fornecedor 2", "estoque": 8, "estoque_minimo": 10
    },
    {
        "referencia": "PB-045", "descricao": "Jaqueta corta vento", "cor": "Preta", "tamanho": "M a GG",
        "genero": "Masculino", "grupo": "Jaquetas", "grade": "M a GG", "data": "14/09/2026",
        "cliente": "PB", "fornecedor": "Fornecedor 2", "estoque": 5, "estoque_minimo": 15
    },
    {
        "referencia": "AC-010", "descricao": "Bermuda moletom", "cor": "Cinza", "tamanho": "38 a 44",
        "genero": "Masculino", "grupo": "Bermudas", "grade": "38 a 44", "data": "27/09/2026",
        "cliente": "AC", "fornecedor": "Fornecedor 3", "estoque": 60, "estoque_minimo": 10
    },
    {
        "referencia": "AC-012", "descricao": "Camiseta estampada", "cor": "Rosa", "tamanho": "P a GG",
        "genero": "Feminino", "grupo": "Camisetas", "grade": "P a GG", "data": "20/09/2026",
        "cliente": "AC", "fornecedor": "Fornecedor 3", "estoque": 120, "estoque_minimo": 10
    },
]

movimentacoes = [
    {
        "data": "16/09/2026", "produto": "DB-001", "tipo": "Entrada", "origem": "Compra",
        "doc_origem": "NF-001", "fornecedor": "Fornecedor 1", "quantidade": 100, "local": "Parado",
        "doc_destino": "", "cliente": "", "usuario": "Cauê Buzolin"
    },
    {
        "data": "16/09/2026", "produto": "PB-032", "tipo": "Saída", "origem": "Venda",
        "doc_origem": "", "fornecedor": "", "quantidade": -50, "local": "Parado",
        "doc_destino": "PED-001", "cliente": "PB", "usuario": "Kauan Constancio"
    },
    {
        "data": "15/09/2026", "produto": "DB-002", "tipo": "Entrada", "origem": "Compra",
        "doc_origem": "NF-002", "fornecedor": "Fornecedor 1", "quantidade": 80, "local": "Parado",
        "doc_destino": "", "cliente": "", "usuario": "Gabriel Guerra"
    },
    {
        "data": "15/09/2026", "produto": "AC-012", "tipo": "Saída", "origem": "Venda",
        "doc_origem": "", "fornecedor": "", "quantidade": -5, "local": "Passadoria",
        "doc_destino": "PED-002", "cliente": "AC", "usuario": "Kaue Giovani"
    },
]

lotes = [
    {"numero": "DB-001", "referencia": "DB-001", "data_entrada": "12/09/2026", "cliente": "DKS", "status": "Em Lavanderia"},
    {"numero": "DB-002", "referencia": "DB-002", "data_entrada": "10/09/2026", "cliente": "DKS", "status": "Recebido"},
    {"numero": "PB-032", "referencia": "PB-032", "data_entrada": "08/09/2026", "cliente": "PB", "status": "Recebido"},
    {"numero": "PB-045", "referencia": "PB-045", "data_entrada": "05/09/2026", "cliente": "AC", "status": "Em Lavanderia"},
    {"numero": "AC-010", "referencia": "AC-010", "data_entrada": "02/09/2026", "cliente": "PB", "status": "Recebido"},
]

ordens = []
