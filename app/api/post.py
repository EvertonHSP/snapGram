from flask_restful import Resource, reqparse
from app.models import Post, Usuario
from app.extensions import db


class PostResource(Resource):

    def get(self, post_id):
        post = Post.query.get(post_id)
        if post:
            return {
                'id': post.id,
                'titulo': post.titulo,
                'conteudo': post.conteudo,
                'data_criacao': post.data_criacao,
                'usuario': post.usuario.username
            }, 200
        return {'message': 'Post not found'}, 404

    def delete(self, post_id):
        post = Post.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return {'message': 'Post deleted'}, 200
        return {'message': 'Post not found'}, 404


class PostListResource(Resource):

    def get(self):
        posts = Post.query.all()
        posts_list = [{
            'id': post.id,
            'titulo': post.titulo,
            'conteudo': post.conteudo,
            'data_criacao': post.data_criacao,
            'usuario': post.usuario.username
        } for post in posts]
        return posts_list, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('titulo', type=str, required=True,
                            help="Title cannot be blank")
        parser.add_argument('conteudo', type=str,
                            required=True, help="Content cannot be blank")
        parser.add_argument('id_usuario', type=int,
                            required=True, help="User ID is required")
        data = parser.parse_args()

        user_id = data.get('id_usuario')
        if not user_id or not isinstance(user_id, int):
            return {'message': 'Invalid user ID'}, 400

        usuario = Usuario.query.get(user_id)
        if not usuario:
            return {'message': 'User not found'}, 404

        new_post = Post(
            titulo=data['titulo'],
            conteudo=data['conteudo'],
            id_usuario=user_id
        )
        db.session.add(new_post)
        db.session.commit()

        return {'message': 'Post created', 'id': new_post.id}, 201
