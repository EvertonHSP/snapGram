from flask import Blueprint
from flask_restful import Api
from app.api.auth import RegisterResource, LoginResource, LogoutResource
from app.api.post import PostResource, PostListResource, CreatePostResource
from app.api.user import UserResource, UserPostsResource, CurrentUserResource, UpdateUserResource
from app.api.comments import ComentarioListResource, CreateComentarioResource
from app.api.likes import PostLikesResource, CurtirPostResource
# Cria o Blueprint para a API
api_bp = Blueprint('api', __name__)

# Cria a instância da API
api = Api(api_bp)

# Rotas de autenticação
api.add_resource(RegisterResource, '/auth/register')
api.add_resource(LoginResource, '/auth/login')
api.add_resource(LogoutResource, '/auth/logout')

# Rotas de usuário
api.add_resource(UserResource, '/user/profile/<int:user_id>')
api.add_resource(UserPostsResource, '/user/posts/<int:user_id>')
api.add_resource(CurrentUserResource, '/user/current')
api.add_resource(UpdateUserResource, '/user/update')

# Rotas de posts
api.add_resource(PostResource, '/post/<int:post_id>')
api.add_resource(PostListResource, '/posts')
api.add_resource(CreatePostResource, '/posts/create')

# Rotas de comentários
api.add_resource(ComentarioListResource, '/post/<int:post_id>/comentarios')
api.add_resource(CreateComentarioResource,
                 '/post/<int:post_id>/comentarios/create')

api.add_resource(PostLikesResource, '/post/<int:post_id>/get_like')
api.add_resource(CurtirPostResource, '/post/<int:post_id>/curtir')

# Função para inicializar a API no app Flask


def init_app(app):
    app.register_blueprint(api_bp, url_prefix='/api')
