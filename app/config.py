# import os


import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'frontend/static/fotos_posts')

    # Chaves secretas
    # Valor padrão se não encontrar no .env
    SECRET_KEY = os.getenv('SECRET_KEY', 'ggttggtt3445634456')
    # Valor padrão se não encontrar no .env
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'wrtt544tghh')

    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    print(f"SECRET_KEY: {SECRET_KEY}")
    print(f"JWT_SECRET_KEY: {JWT_SECRET_KEY}")
    print(f"SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")
    print(f"UPLOAD_FOLDER: {UPLOAD_FOLDER}")


'''
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '2dd1e09fe4e5058af539002a4da59b84')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://postgres:1@localhost:5051/snapgram')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Corrigido: faltava uma vírgula no final
    UPLOAD_FOLDER = "frontend/static/fotos_posts"
'''
