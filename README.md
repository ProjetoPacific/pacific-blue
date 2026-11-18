# Pacific Blue — Sistema de Gestão de Estoque

Sistema web para controlar o estoque da marca **Pacific Blue**: produtos, entradas e saídas,
lotes, ordens de produção e clientes, com histórico completo de quem mexeu em quê.

Projeto integrador da **Fatec Taquaritinga** — Análise e Desenvolvimento de Sistemas.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-banco%20local-003B57?logo=sqlite&logoColor=white)

## O problema

Com o estoque em papel ou planilha, ninguém tem certeza do saldo, o estoque baixo só aparece
quando a peça já faltou e não existe histórico de quem fez cada alteração.

## A solução

O Pacific Blue mostra o **saldo em tempo real**, registra cada **entrada e saída com o
responsável**, controla **lotes** e **ordens de produção** e **alerta quando o estoque está
baixo**. O caminho de uma peça fica todo registrado: cadastro do produto, entrada, ordens e
processos, saída — sempre com data e usuário.

## Módulos

| Módulo | O que faz |
|---|---|
| **Acesso** | Login, cadastro de conta, recuperação e alteração de senha, lista de usuários |
| **Dashboard** | Total de produtos e de peças, entradas e saídas, alerta de estoque baixo e últimas movimentações |
| **Produtos** | Cadastro, busca, filtro por grupo e por cliente, edição e exclusão |
| **Movimentação** | Entradas e saídas de estoque, com ordem de produção, cliente e processo |
| **Histórico** | Todas as movimentações, com filtro por tipo, data e busca (telas separadas de entradas e saídas) |
| **Lotes** | Controle de lotes por referência de produto, com status |
| **Ordens de produção** | Ordens com um ou mais processos, local e datas |
| **Clientes** | Cadastro completo de clientes |
| **Tecnologias** | Página com as tecnologias usadas no projeto |

## Regras de negócio

- Saída maior que o saldo disponível é barrada (e o banco também impede estoque negativo).
- Referência de produto, código de cliente, número de lote e de ordem não podem se repetir.
- Ajuste de saldo na edição do produto gera uma movimentação do tipo **Ajuste** no histórico.
- Produto e cliente só podem ser excluídos se não tiverem vínculos; lote só pode ser excluído
  se estiver **Concluído**.
- Saldo e histórico são gravados juntos, na mesma transação: ou grava os dois, ou nenhum.
- Todas as telas exigem login; sem entrar, qualquer endereço volta para a tela de login.

## Tecnologias

- **Python** e **Flask** (organização em *Blueprints*, um por módulo)
- **Jinja2** para as páginas HTML e **CSS** responsivo
- **SQLite** (módulo `sqlite3` do próprio Python), sem servidor de banco
- **Git** e **VS Code**

**Por que Flask?** É leve, simples e deixa a organização do projeto na mão da equipe.
**Por que SQLite?** Não precisa de servidor, já vem com o Python, guarda tudo em um único
arquivo e o backup é só copiar esse arquivo.

## Estrutura do projeto

```
pacific-blue/
├── backend/                  servidor Flask, regras de negócio e banco de dados
│   ├── main.py               cria o app, registra os módulos e inicia o banco
│   ├── banco.py              conexão, transações, criação das tabelas e carga inicial
│   ├── dados.py              dados de demonstração e opções dos formulários
│   ├── datas.py              funções de data
│   ├── controller/           um arquivo de rotas para cada módulo
│   ├── tests/                testes automatizados (pytest)
│   ├── requirements.txt      dependências para rodar
│   └── requirements-dev.txt  dependências para rodar os testes
├── frontend/                 o que aparece no navegador
│   ├── templates/            páginas HTML (Jinja2); base.html guarda o menu
│   └── static/css/           estilos
├── web/                      reservada para um cliente web separado (ainda vazia)
├── mobile/                   reservada para o aplicativo mobile (ainda vazia)
└── .vscode/launch.json       configuração para rodar e depurar no VS Code
```

**Caminho de uma requisição:** navegador → rota no *controller* → consulta ao banco →
template Jinja2 → HTML de volta ao navegador. O menu é escrito uma única vez, em
`base.html`, e todas as páginas o reaproveitam com `{% extends 'base.html' %}`.

## Como executar

Pré-requisito: **Python 3.10 ou superior**.

1. Baixe o projeto:
   ```bash
   git clone https://github.com/ProjetoPacific/pacific-blue.git
   cd pacific-blue/backend
   ```
2. (Recomendado) crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   # Windows:      .venv\Scripts\activate
   # Linux e Mac:  source .venv/bin/activate
   ```
3. Instale as dependências e inicie o servidor:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```
4. Abra no navegador: **http://127.0.0.1:9000**

**No VS Code:** abra a pasta do projeto, vá em *Executar e Depurar* e escolha
**Pacific Blue (backend)**.

### Login para testar

| Usuário | Senha |
|---------|-------|
| caue | 1234 |
| kauan | 1234 |
| gabriel | 1234 |
| kaue | 1234 |
| mahmoud | 1234 |

Na primeira execução o sistema já vem com dados de demonstração: **6 produtos e 621 peças**,
com alerta de estoque baixo para **PB-032** e **PB-045**.

### Configuração opcional

O sistema funciona sem configurar nada. Para uso fora de um computador de estudo, defina
variáveis de ambiente antes de iniciar:

| Variável | Para que serve | Padrão |
|---|---|---|
| `SECRET_KEY` | Chave que protege a sessão de login. **Troque em qualquer uso real.** | `pacificblue` |
| `FLASK_DEBUG` | Use `0` para desligar o modo debug | ligado |
| `PACIFIC_BLUE_DB` | Caminho do arquivo do banco de dados | `backend/pacific_blue.db` |

Exemplo (Linux e Mac): `SECRET_KEY="uma-chave-longa" FLASK_DEBUG=0 python main.py`

## Banco de dados

Os dados ficam no arquivo `backend/pacific_blue.db`, criado sozinho na primeira execução. Cada
alteração é gravada na hora, então fechar o programa (ou até derrubar o servidor à força)
não perde nada.

**Tabelas:** `usuarios`, `clientes`, `produtos`, `movimentacoes`, `lotes`, `ordens` e
`ordens_processos`.

**Relações:**
- Uma ordem tem vários processos (1 para N), com chave estrangeira e exclusão em cascata.
- Produto liga com movimentações, lotes e ordens pela **referência**.
- Cliente liga com produtos, lotes, movimentações e ordens pelo **nome**.

**Proteções no próprio banco:** referência de produto única e `CHECK (estoque >= 0)`.

**Dúvidas comuns:**
- *Como voltar aos dados de demonstração?* Feche o programa e apague o arquivo `.db`.
- *Como fazer backup?* Copie o arquivo `pacific_blue.db` com o programa fechado.
- *Posso editar `dados.py` para mudar os dados?* Só vale para um banco novo: as listas são
  usadas apenas na primeira execução.
- O arquivo `.db` não vai para o Git; cada pessoa tem o seu.

## Testes automatizados

Os testes cobrem login, proteção das telas, regras de estoque, exclusões bloqueadas e
persistência. Eles usam um banco temporário e **não mexem no seu `pacific_blue.db`**.

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest
```

## Limitações e próximos passos

Este projeto é uma versão de estudo. Para virar um sistema de produção, os próximos passos são:

- **Senhas em texto puro** no banco: guardar com *hash* (por exemplo, `werkzeug.security`).
- **Chave secreta e debug:** já podem ser configurados por variável de ambiente, mas o padrão
  de estudo continua inseguro.
- **Cliente ligado pelo nome:** trocar por chave estrangeira com o ID do cliente.
- **Sem perfis de permissão:** todo usuário logado pode fazer tudo.
- **SQLite** atende poucos usuários ao mesmo tempo; para crescer, migrar para PostgreSQL ou MySQL.
- **Sem API:** é ela que permitiria preencher as pastas `web/` e `mobile/`.
- **SQL escrito direto:** um próximo passo seria um ORM como o SQLAlchemy.

## Equipe

Cauê Buzolin, Kauan Constancio, Gabriel Guerra, Kaue Giovani e Mahmoud Rkaine.
