from flask import Flask, request
from flask_cors import CORS  # Importe o CORS
from app.config import Config
from app.extensions import db, bcrypt, migrate
from app.api import init_app as init_api
from flask_jwt_extended import JWTManager, jwt_required
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def create_app():
    # Cria a instância do Flask
    app = Flask(__name__)
    
    # Carrega as configurações
    app.config.from_object(Config)

    # Configura o CORS para permitir qualquer origem
    CORS(app)  # Permite requisições de qualquer origem

    
    # Inicializa as extensões
    jwt = JWTManager(app)  # Configura o JWT
    

    
    @app.route('/test', methods=['GET'])
    @jwt_required()
    def test():
            return {"message": "Token válido!"}, 200

    @app.before_request
    def log_request_info():
        from flask import current_app  
        print(f"Chave secreta usada para validar o token: {app.config['JWT_SECRET_KEY']}")
        print(f"Chave secreta usada para validar o token: {current_app.config['JWT_SECRET_KEY']}")
        print("\n--- Nova Requisição ---")
        print("Método:", request.method)
        print("Cabeçalhos:", request.headers)
        print("Corpo da Requisição:", request.get_data())
        print("-----------------------\n")

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Inicializa a API
    init_api(app)

    return app