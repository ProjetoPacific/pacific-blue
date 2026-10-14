<<<<<<< HEAD
# inicia o site e conecta todos os controllers
=======
#inicia o site e conecta todos os controllers
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861

from flask import Flask
from controller.login_controller import login_bp
from controller.dashboard_controller import dashboard_bp
from controller.produtos_controller import produtos_bp
from controller.movimentacao_controller import movimentacao_bp
<<<<<<< HEAD
from controller.historico_controller import historico_bp
from controller.lotes_controller import lotes_bp
=======
from controller.lotes_controller import lotes_bp
from controller.historico_controller import historico_bp
from controller.relatorios_controller import relatorios_bp
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
from controller.usuarios_controller import usuarios_bp
from controller.clientes_controller import clientes_bp
from controller.ordens_controller import ordens_bp

app = Flask(__name__)
app.secret_key = "pacificblue"

app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(produtos_bp)
app.register_blueprint(movimentacao_bp)
<<<<<<< HEAD
app.register_blueprint(historico_bp)
app.register_blueprint(lotes_bp)
=======
app.register_blueprint(lotes_bp)
app.register_blueprint(historico_bp)
app.register_blueprint(relatorios_bp)
>>>>>>> 17fd6b1368a91262f521c0b84770b833fd125861
app.register_blueprint(usuarios_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(ordens_bp)

if __name__ == "__main__":
    app.run(port=9000, debug=True)
