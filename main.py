from flask import Flask
from app.route import bp as route_bp  # Importa o Blueprint


def create_app():
    app = Flask(__name__)

    # Definindo configurações diretamente no main.py
    app.config['SECRET_KEY'] = '6r45yera5y4e85y8e5'
    app.config['UPLOAD_FOLDER'] = './upload/'

    # Registrando o Blueprint
    app.register_blueprint(route_bp)

    return app


if __name__ == '__main__':
    app = create_app()  # Cria a instância do app
