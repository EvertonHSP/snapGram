# app/_init_:
from flask import Flask
from app.config import Config
from app.extensions import db, bcrypt, login_manager, migrate
from app.api import init_app as init_api
from app.routes import routes
from app.models import Usuario
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
    print(f"Template Directory: {TEMPLATE_DIR}")
    print(f"Static Directory: {STATIC_DIR}")

    JWTManager(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "routes.homepage"

    init_api(app)

    app.register_blueprint(routes)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app
