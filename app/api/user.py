from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Usuario, Post
import re


class UserResource(Resource):
    def get(self, user_id):
        usuario = Usuario.query.get(user_id)
        if not usuario:
            return {"error": "Usuário não encontrado"}, 404

        return {
            "id": usuario.id,
            "username": usuario.username
        }, 200


class UserPostsResource(Resource):
    def get(self, user_id):
        usuario = Usuario.query.get(user_id)
        if not usuario:
            return {"error": "Usuário não encontrado"}, 404

        posts = Post.query.filter_by(id_usuario=user_id).all()
        posts_data = [{
            "id": post.id,
            "titulo": post.titulo,
            "conteudo": post.conteudo,
            "data_criacao": post.data_criacao.isoformat()
        } for post in posts]

        return {"posts": posts_data}, 200


class CurrentUserResource(Resource):
    @jwt_required()
    def get(self):
        print("def get(self):")
        user_id = get_jwt_identity()
        usuario = Usuario.query.get(user_id)

        if not usuario:
            print("Usuário não encontrado")
            return {"error": "Usuário não encontrado"}, 404
            
        return {
            "id": usuario.id,
            "username": usuario.username,
            "email": usuario.email
        }, 200


class UpdateUserResource(Resource):
    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        usuario = Usuario.query.get(user_id)

        if not usuario:
            return {"error": "Usuário não encontrado"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=False, trim=True)
        parser.add_argument('email', type=str, required=False, trim=True)
        data = parser.parse_args()

        if not any([data.get('username'), data.get('email')]):
            return {"error": "Nenhum dado foi enviado para atualização"}, 400

        if data.get('username'):
            usuario.username = data['username']

        if data.get('email'):
            if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
                return {"error": "E-mail inválido"}, 400
            usuario.email = data['email']

        db.session.commit()

        return {
            "status": "success",
            "message": "Usuário atualizado com sucesso",
            "data": {
                "id": usuario.id,
                "username": usuario.username,
                "email": usuario.email
            }
        }, 200
