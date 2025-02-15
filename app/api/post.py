from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Post, Usuario


class PostListResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('limit', type=int, default=10)
        parser.add_argument('user_id', type=int, required=False)
        args = parser.parse_args()

        query = Post.query
        if args['user_id']:
            query = query.filter_by(id_usuario=args['user_id'])

        posts = query.order_by(Post.data_criacao.desc()).paginate(
            page=args['page'], per_page=args['limit'], error_out=False)

        return {
            "posts": [{
                "id": post.id,
                "titulo": post.titulo,
                "conteudo": post.conteudo,
                "data_criacao": post.data_criacao.isoformat(),
                "id_usuario": post.id_usuario
            } for post in posts.items],
            "total": posts.total,
            "page": posts.page,
            "pages": posts.pages
        }, 200


class PostResource(Resource):
    def get(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            return {"error": "Post não encontrado"}, 404

        return {
            "id": post.id,
            "titulo": post.titulo,
            "conteudo": post.conteudo,
            "data_criacao": post.data_criacao.isoformat(),
            "id_usuario": post.id_usuario
        }, 200

    @jwt_required()
    def delete(self, post_id):
        user_id = get_jwt_identity()
        post = Post.query.get(post_id)

        if not post:
            return {"error": "Post não encontrado"}, 404

        if post.id_usuario != user_id:
            return {"error": "Apenas o autor pode deletar este post"}, 403

        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deletado com sucesso"}, 200


class CreatePostResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        usuario = Usuario.query.get(user_id)

        if not usuario:
            return {"error": "Usuário não encontrado"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('titulo', type=str, required=True,
                            help="Título é obrigatório")
        parser.add_argument('conteudo', type=str,
                            required=True, help="Conteúdo é obrigatório")
        args = parser.parse_args()

        novo_post = Post(
            titulo=args['titulo'],
            conteudo=args['conteudo'],
            id_usuario=user_id
        )

        db.session.add(novo_post)
        db.session.commit()

        return {
            "message": "Post criado com sucesso",
            "post": {
                "id": novo_post.id,
                "titulo": novo_post.titulo,
                "conteudo": novo_post.conteudo,
                "data_criacao": novo_post.data_criacao.isoformat(),
                "id_usuario": novo_post.id_usuario
            }
        }, 201
