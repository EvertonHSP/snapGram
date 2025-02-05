# app/_init_:
from flask import Flask
from app.config import Config
from app.extensions import db, bcrypt, login_manager, migrate
from app.api import init_app as init_api
from app.routes import routes
from app.models import Usuario  # Importação correta para evitar ciclo
from flask_jwt_extended import JWTManager
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def create_app():
    TEMPLATE_DIR = os.path.abspath(
        os.path.join(BASE_DIR, "frontend/templates"))
    STATIC_DIR = os.path.abspath(
        os.path.join(BASE_DIR, "frontend/static"))

    app = Flask(__name__, template_folder=TEMPLATE_DIR,
                static_folder=STATIC_DIR)
    app.config.from_object(Config)
    print(f"Template Directory: {TEMPLATE_DIR}")  # Adicione esta linha
    print(f"Static Directory: {STATIC_DIR}")  # Adicione esta linha
    # Inicializa as extensões

    JWTManager(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Define a página de login padrão
    login_manager.login_view = "routes.homepage"  # Atualize conforme necessário  # noqa: E501

    # Inicializa a API (Blueprints e Flask-RESTful)
    init_api(app)

    # Registra as rotas como um Blueprint
    app.register_blueprint(routes)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app


# C:\Users\compa\Documents\Everton\snapGram\frontend\templates\homepage.html
# C:\Users\compa\Documents\Everton\snapGram\app\frontend\templates
"""from flask import Flask
from app.config import Config
from app.extensions import database, bcrypt, login_manager, migrate
from app.api.auth import auth_bp as auth_api
from app.api.user import user_bp as user_api
from app.api.post import api as post_api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Carrega as coo config.py

    with app.app_context():
        database.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        migrate.init_app(app, database)
    login_manager.login_view = "api.auth.login"
    # Define a rota de login para usuários não autenticados

    # Registra os Blueprints
    app.register_blueprint(auth_api, url_prefix='/api/auth')
    app.register_blueprint(user_api, url_prefix='/api/user')
    app.register_blueprint(post_api, url_prefix='/api/post')

    return app
"""


"""from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.config import Config  # Importando a nova configuração

# Inicializa o app
app = Flask(__name__)
app.config.from_object(Config)  # Carrega a configuração do config.py

# Inicializa extensões
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Usuário não logado é direcionado para a homepage
login_manager.login_view = "homepage"
"""

"""from flask import Flask
from app import routes
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask( __name__ )

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///snapgram.db"
app.config['SECRET_KEY'] = "2dd1e09fe4e5058af539002a4da59b84"
app.config['UPLOAD_FOLDER'] = "static/fotos_posts"

database = SQLAlchemy( app )

bcrypt = Bcrypt( app )
login_manager = LoginManager( app )

# usuário não logado é direcionado para a rota principal, no caso "homepage"
login_manager.login_view = "homepage"
"""
