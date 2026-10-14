<<<<<<< HEAD
# onde ficam os dados
=======
#onde ficam os dados
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

usuarios = [
    {"usuario": "caue", "senha": "1234", "nome": "Cauê Buzolin", "email": "caue@email.com"},
    {"usuario": "kauan", "senha": "1234", "nome": "Kauan Constancio", "email": "kauan@email.com"},
    {"usuario": "gabriel", "senha": "1234", "nome": "Gabriel Guerra", "email": "gabriel@email.com"},
    {"usuario": "kaue", "senha": "1234", "nome": "Kaue Giovani", "email": "kaue@email.com"},
    {"usuario": "mahmoud", "senha": "1234", "nome": "Mahmoud Rkaine", "email": "mahmoud@email.com"},
]

clientes = [
    {"nome": "DKS", "telefone": "-", "email": "-"},
    {"nome": "PB", "telefone": "-", "email": "-"},
    {"nome": "AC", "telefone": "-", "email": "-"},
]

<<<<<<< HEAD
# Opções usadas nos campos de seleção.
fornecedores = ["Fornecedor 1", "Fornecedor 2", "Fornecedor 3"]

# Opções de origem para cada tipo de movimentação.
origens_movimentacao = {
    "Entrada": ["Compra", "Ajuste", "Devolução"],
    "Saída": ["Venda", "Ajuste"],
}
=======
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
grupos = ["Calças", "Camisetas", "Jaquetas", "Bermudas"]
generos = ["Masculino", "Feminino", "Unissex"]
locais = ["Parado", "Lavanderia", "Laser", "Used", "Passadoria", "Manual"]
processos = ["Destroyed", "Used local", "Bigode laser"]

<<<<<<< HEAD
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
=======
motivos_movimentacao = {
    "Entrada": ["Compra", "Devolução", "Correção"],
    "Saída": ["Venda", "Correção"],
    "Ajuste": ["Compra", "Venda", "Devolução", "Correção"],
}

produtos = [
    {
        "referencia": "DB-001", "ncm": "6203.42.00", "nome": "Calça Jeans", "descricao": "Calça jeans reta",
        "grupo": "Calças", "estilo": "Reta", "cliente": "DKS", "genero": "Masculino", "cor": "Azul",
        "tamanhos": "36 a 48", "tecido": "Denim", "composicao": "100% algodão",
        "estoque": 248, "estoque_minimo": 10, "data_estoque": "16/09/2026"
    },
    {
        "referencia": "DB-002", "ncm": "6204.62.00", "nome": "Calça Jeans", "descricao": "Calça jeans skinny",
        "grupo": "Calças", "estilo": "Skinny", "cliente": "DKS", "genero": "Feminino", "cor": "Azul",
        "tamanhos": "36 a 46", "tecido": "Denim", "composicao": "98% algodão, 2% elastano",
        "estoque": 180, "estoque_minimo": 15, "data_estoque": "15/09/2026"
    },
    {
        "referencia": "PB-032", "ncm": "6109.10.00", "nome": "Camiseta", "descricao": "Camiseta básica",
        "grupo": "Camisetas", "estilo": "Básica", "cliente": "PB", "genero": "Unissex", "cor": "Branca",
        "tamanhos": "P a GG", "tecido": "Malha", "composicao": "100% algodão",
        "estoque": 8, "estoque_minimo": 10, "data_estoque": "16/09/2026"
    },
    {
        "referencia": "PB-045", "ncm": "6201.93.00", "nome": "Jaqueta", "descricao": "Jaqueta corta vento",
        "grupo": "Jaquetas", "estilo": "Corta vento", "cliente": "PB", "genero": "Masculino", "cor": "Preta",
        "tamanhos": "M a GG", "tecido": "Nylon", "composicao": "100% poliamida",
        "estoque": 5, "estoque_minimo": 15, "data_estoque": "14/09/2026"
    },
    {
        "referencia": "AC-010", "ncm": "6203.42.00", "nome": "Bermuda", "descricao": "Bermuda moletom",
        "grupo": "Bermudas", "estilo": "Esportiva", "cliente": "AC", "genero": "Masculino", "cor": "Cinza",
        "tamanhos": "38 a 44", "tecido": "Moletom", "composicao": "80% algodão, 20% poliéster",
        "estoque": 60, "estoque_minimo": 10, "data_estoque": "27/09/2026"
    },
    {
        "referencia": "AC-012", "ncm": "6109.10.00", "nome": "Camiseta", "descricao": "Camiseta estampada",
        "grupo": "Camisetas", "estilo": "Estampada", "cliente": "AC", "genero": "Feminino", "cor": "Rosa",
        "tamanhos": "P a GG", "tecido": "Malha", "composicao": "100% algodão",
        "estoque": 120, "estoque_minimo": 10, "data_estoque": "20/09/2026"
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
    },
]

movimentacoes = [
<<<<<<< HEAD
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
=======
    {"data": "16/09/2026", "produto": "DB-001", "tipo": "Entrada", "motivo": "Compra", "quantidade": 100, "usuario": "Cauê Buzolin", "observacao": ""},
    {"data": "16/09/2026", "produto": "PB-032", "tipo": "Saída", "motivo": "Venda", "quantidade": -50, "usuario": "Kauan Constancio", "observacao": ""},
    {"data": "15/09/2026", "produto": "DB-002", "tipo": "Entrada", "motivo": "Compra", "quantidade": 80, "usuario": "Gabriel Guerra", "observacao": ""},
    {"data": "15/09/2026", "produto": "DB-001", "tipo": "Ajuste", "motivo": "Correção", "quantidade": -20, "usuario": "Kaue Giovani", "observacao": ""},
    {"data": "15/09/2026", "produto": "PB-032", "tipo": "Ajuste", "motivo": "Devolução", "quantidade": -5, "usuario": "Mahmoud Rkaine", "observacao": ""},
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
]

lotes = [
    {"numero": "L001", "data_entrada": "12/09/2026", "cliente": "DKS", "status": "Em Lavanderia"},
    {"numero": "L002", "data_entrada": "10/09/2026", "cliente": "DKS", "status": "Recebido"},
    {"numero": "L003", "data_entrada": "08/09/2026", "cliente": "PB", "status": "Recebido"},
    {"numero": "L004", "data_entrada": "05/09/2026", "cliente": "AC", "status": "Em Lavanderia"},
    {"numero": "L005", "data_entrada": "02/09/2026", "cliente": "PB", "status": "Recebido"},
]

ordens = [
    {
        "numero": "0001", "referencia": "DB-001", "cliente": "DKS", "quantidade": 88, "processo": "Used local",
        "local": "Lavanderia", "data_local": "12/09/2026", "status": "Em produção", "destino": "",
        "fluxo": [{"local": "Parado", "data": "08/09/2026"}, {"local": "Lavanderia", "data": "12/09/2026"}]
    },
    {
        "numero": "0002", "referencia": "PB-032", "cliente": "PB", "quantidade": 50, "processo": "Destroyed",
        "local": "Laser", "data_local": "24/09/2026", "status": "Em produção", "destino": "",
        "fluxo": [{"local": "Parado", "data": "15/09/2026"}, {"local": "Lavanderia", "data": "18/09/2026"}, {"local": "Laser", "data": "24/09/2026"}]
    },
    {
        "numero": "0003", "referencia": "DB-002", "cliente": "DKS", "quantidade": 80, "processo": "Bigode laser",
        "local": "Passadoria", "data_local": "22/09/2026", "status": "Em produção", "destino": "",
        "fluxo": [{"local": "Parado", "data": "10/09/2026"}, {"local": "Lavanderia", "data": "14/09/2026"}, {"local": "Laser", "data": "18/09/2026"}, {"local": "Passadoria", "data": "22/09/2026"}]
    },
    {
        "numero": "0004", "referencia": "AC-010", "cliente": "AC", "quantidade": 60, "processo": "Used local",
        "local": "Parado", "data_local": "27/09/2026", "status": "Em produção", "destino": "",
        "fluxo": [{"local": "Parado", "data": "27/09/2026"}]
    },
    {
        "numero": "0005", "referencia": "AC-012", "cliente": "AC", "quantidade": 120, "processo": "Used local",
        "local": "Saída", "data_local": "20/09/2026", "status": "Finalizada", "destino": "AC",
        "fluxo": [{"local": "Parado", "data": "05/09/2026"}, {"local": "Manual", "data": "10/09/2026"}, {"local": "Passadoria", "data": "16/09/2026"}, {"local": "Saída para AC", "data": "20/09/2026"}]
    },
]
