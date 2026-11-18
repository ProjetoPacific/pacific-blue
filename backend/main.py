# inicia o site e conecta todos os controllers

import os

from flask import Flask
import banco
from controller.login_controller import login_bp
from controller.dashboard_controller import dashboard_bp
from controller.produtos_controller import produtos_bp
from controller.movimentacao_controller import movimentacao_bp
from controller.historico_controller import historico_bp
from controller.lotes_controller import lotes_bp
from controller.usuarios_controller import usuarios_bp
from controller.clientes_controller import clientes_bp
from controller.ordens_controller import ordens_bp
from controller.tecnologias_controller import tecnologias_bp

# as telas (HTML/CSS) ficam na pasta frontend, ao lado do backend
FRONTEND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")

app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND, "templates"),
    static_folder=os.path.join(FRONTEND, "static"),
)
# em uso real, defina a variável de ambiente SECRET_KEY (o padrão serve só para estudo)
app.secret_key = os.environ.get("SECRET_KEY", "pacificblue")

# cria o banco (pacific_blue.db) na primeira execução e fecha a conexão ao fim de cada requisição
banco.iniciar_banco()
app.teardown_appcontext(banco.fechar_banco)

app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(produtos_bp)
app.register_blueprint(movimentacao_bp)
app.register_blueprint(historico_bp)
app.register_blueprint(lotes_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(ordens_bp)
app.register_blueprint(tecnologias_bp)

if __name__ == "__main__":
    print("Banco de dados:", banco.CAMINHO_BANCO)
    # FLASK_DEBUG=0 desliga o modo debug
    app.run(port=9000, debug=os.environ.get("FLASK_DEBUG", "1") != "0")
