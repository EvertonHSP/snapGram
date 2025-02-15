from flask import Blueprint
from flask_restful import Api
from app.api.auth import RegisterResource, LoginResource, LogoutResource
from app.api.post import PostResource, PostListResource
from app.api.user import UserResource, UserPostsResource, CurrentUserResource, UpdateUserResource

# Cria o Blueprint para a API
api_bp = Blueprint('api', __name__)

# Cria a instância da API
api = Api(api_bp)

# Rotas de autenticação
api.add_resource(RegisterResource, '/auth/register')
api.add_resource(LoginResource, '/auth/login')
api.add_resource(LogoutResource, '/auth/logout')

# Rotas de usuário
api.add_resource(UserResource, '/user/profile/<int:user_id>')  # Rota para obter informações de um usuário específico
api.add_resource(UserPostsResource, '/user/posts/<int:user_id>')  # Rota para obter os posts de um usuário específico
api.add_resource(CurrentUserResource, '/user/current')  # Rota para obter informações do usuário atual (autenticado)
api.add_resource(UpdateUserResource, '/user/update')  # Rota para atualizar informações do usuário

# Rotas de posts
api.add_resource(PostResource, '/post/<int:post_id>')  # Rota para obter, atualizar ou deletar um post específico
api.add_resource(PostListResource, '/posts')  # Rota para listar todos os posts ou criar um novo post

# Função para inicializar a API no app Flask
def init_app(app):
    app.register_blueprint(api_bp, url_prefix='/api')