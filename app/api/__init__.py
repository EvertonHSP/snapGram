from flask import Blueprint
from flask_restful import Api
# Importa os recursos de autenticação
from app.api.auth import RegisterResource, LoginResource, LogoutResource
# Importa os recursos de post
from app.api.post import PostResource, PostListResource
# Importa os recursos de usuário
from app.api.user import ProfileResource, UpdateResource

# Criação do Blueprint para a API
api_bp = Blueprint('api', __name__)

# Inicializando o Flask-RESTful API
api = Api(api_bp)

# Definindo as rotas do Flask-RESTful para os recursos
api.add_resource(RegisterResource, '/auth/register')  # Registro de usuário
api.add_resource(LoginResource, '/auth/login')  # Login de usuário
api.add_resource(LogoutResource, '/auth/logout')  # Logout de usuário
api.add_resource(ProfileResource, '/user/profile')
# Perfil do usuário autenticado
api.add_resource(UpdateResource, '/user/update')
# Atualização de dados do usuário
api.add_resource(PostResource, '/post/<int:post_id>')
# Endpoint para um post específico
api.add_resource(PostListResource, '/posts')  # Lista de posts

# Registrar o Blueprint na aplicação principal


def init_app(app):
    app.register_blueprint(api_bp, url_prefix='/api')
    # Registra o Blueprint da API com o prefixo '/api'


'''from flask import Blueprint
from flask_restful import Api
from app.api.auth import auth_bp  # Importa o Blueprint de autenticação
from app.api.user import UserResource  # Importa o Resource de usuário
from app.api.post import PostResource  # Importa o Resource de post

# Criação do Blueprint para a API
api_bp = Blueprint('api', __name__)

# Inicializando o Flask-RESTful API
api = Api(api_bp)

# Definindo as rotas do Flask-RESTful
api.add_resource(UserResource, '/user/<int:user_id>')
# Endpoint para um único usuário
api.add_resource(PostResource, '/post/<int:post_id>')
# Endpoint para um post específico

# Registrar o Blueprint na aplicação principal
def init_app(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    # Registra o Blueprint de autenticação
    app.register_blueprint(api_bp, url_prefix='/api
    # Registra o Blueprint da API
'''
"""from flask import Blueprint
from flask_restful import Api
from app.api.auth import auth_bp
from app.api.user import user_bp
from app.api.post import PostResource

# Criação do Blueprint para a API
api_bp = Blueprint('api', __name__)

# Inicializando o Flask-RESTful API
api = Api(api_bp)

# Definindo as rotas
api.add_resource(auth_bp, '/auth')  # Endpoint para autenticação
api.add_resource(user_bp, '/user/<int:user_id>')
# Endpoint para um único usuário
api.add_resource(PostResource, '/post/<int:post_id>')
# Endpoint para um post específico

# Registrar o Blueprint na aplicação principal
def init_app(app):
    app.register_blueprint(api_bp, url_prefix='/api')
"""
