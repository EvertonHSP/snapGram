
import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'frontend/static/fotos_posts')
    SECRET_KEY = os.getenv('SECRET_KEY', 'ggttggtt3445634456')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'wrtt544tghh')
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
