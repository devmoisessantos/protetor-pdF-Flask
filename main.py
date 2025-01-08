import os
from flask import Flask
from app.route import bp as route_bp  # Importa o Blueprint


def create_app():
    app = Flask(__name__)

    # Definindo configurações diretamente no main.py
    app.config['SECRET_KEY'] = '6r45yera5y4e85y8e5'

    # Caminho absoluto para a pasta de uploads
    upload_folder = os.path.abspath('./uploads/')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    app.config['UPLOAD_FOLDER'] = upload_folder

    # Registrando o Blueprint
    app.register_blueprint(route_bp)

    return app


app = create_app()  # Expondo a instância para o Gunicorn

if __name__ == '__main__':
    app.run()  # Executando apenas para desenvolvimento local
