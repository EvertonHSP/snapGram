from flask import Blueprint
from flask_restful import Api
from app.api.auth import RegisterResource, LoginResource, LogoutResource
from app.api.post import PostResource, PostListResource

from app.api.user import ProfileResource, UpdateResource


api_bp = Blueprint('api', __name__)


api = Api(api_bp)


api.add_resource(RegisterResource, '/auth/register')
api.add_resource(LoginResource, '/auth/login')
api.add_resource(LogoutResource, '/auth/logout')
api.add_resource(ProfileResource, '/user/profile')
api.add_resource(UpdateResource, '/user/update')
api.add_resource(PostResource, '/post/<int:post_id>')
api.add_resource(PostListResource, '/posts')


def init_app(app):
    app.register_blueprint(api_bp, url_prefix='/api')
