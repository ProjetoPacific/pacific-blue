# Pacific Blue — Sistema de Gestão de Estoque

Site para controlar o estoque de roupas da marca **Pacific Blue**: produtos, movimentações
(entrada, saída e ajuste), clientes, lotes de lavanderia e ordens de produção.

Projeto da Fatec Taquaritinga — Análise e Desenvolvimento de Sistemas.

**Tecnologias:** Python, Flask, SQLite, HTML (Jinja2) e CSS.

## Funcionalidades

- Login, cadastro de conta, recuperação e alteração de senha
- Cadastro e consulta de produtos e clientes
- Movimentação de estoque (entrada, saída e ajuste), com motivos por tipo
- Bloqueio de saída maior que o estoque disponível
- Lotes de lavanderia
- Ordens de produção com processo, local, dias no local e fluxo
- Histórico de movimentações e dashboard
- Cadastro de tecnologias

## Estrutura do projeto

```
pacific-blue/
├── backend/      servidor Flask, regras de negócio e banco de dados
│   ├── main.py          inicia o site
│   ├── banco.py         conexão e criação do banco SQLite
│   ├── dados.py         dados de demonstração e opções dos formulários
│   ├── datas.py         funções de data
│   ├── controller/      rotas de cada área do sistema
│   └── requirements.txt
├── frontend/     o que aparece no navegador
│   ├── templates/       páginas HTML
│   └── static/css/      estilos
├── web/          reservado para um cliente web separado (ainda vazio)
├── mobile/       reservado para o aplicativo mobile (ainda vazio)
└── README.md
```

## Como executar

1. Instale o Python 3.10 ou superior.
2. No terminal, dentro da pasta do projeto:
   ```
   cd backend
   pip install -r requirements.txt
   python main.py
   ```
3. Abra no navegador: http://127.0.0.1:9000

**No VS Code:** abra a pasta do projeto, vá em *Executar e Depurar* e escolha
**Pacific Blue (backend)**.

## Login para testar

| Usuário | Senha |
|---------|-------|
| caue | 1234 |
| kauan | 1234 |
| gabriel | 1234 |
| kaue | 1234 |
| mahmoud | 1234 |

## Banco de dados

- Os dados ficam no arquivo `backend/pacific_blue.db`, criado sozinho na primeira execução
  com os dados de demonstração de `dados.py`.
- Tudo o que você cadastra é salvo na hora e continua lá quando o programa é reaberto.
- Para voltar aos dados de demonstração, feche o programa e apague o arquivo `.db`.
- As listas de `dados.py` só servem para criar o banco na primeira vez. Alterá-las não muda
  um banco que já existe.
- O arquivo `.db` não vai para o Git.

## Equipe

Cauê Buzolin, Kauan Constancio, Gabriel Guerra, Kaue Giovani e Mahmoud Rkaine.

## Limitações

Este projeto é uma versão de estudo. Em um sistema real, seria preciso guardar as senhas
criptografadas (hoje ficam em texto no banco), trocar a chave secreta do `main.py` e desligar
o modo debug.
