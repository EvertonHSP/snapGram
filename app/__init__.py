from flask import Flask, request
from flask_cors import CORS  
from app.config import Config
from app.extensions import db, bcrypt, migrate
from app.api import init_app as init_api
from flask_jwt_extended import JWTManager, jwt_required
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app) 
    jwt = JWTManager(app)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    init_api(app)
    from app.routesUploadedFile import upload_bp
    app.register_blueprint(upload_bp)

    return app
