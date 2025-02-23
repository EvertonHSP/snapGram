from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Comentario, Post, Usuario
from app.extensions import db
from datetime import datetime


class ComentarioListResource(Resource):
    def get(self, post_id):
        # Verifica se o post existe
        post = Post.query.get(post_id)
        if not post:
            return {"error": "Post não encontrado"}, 404

        # Configura o parser para paginação
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('limit', type=int, default=10, location='args')
        args = parser.parse_args()

        # Busca os comentários do post com paginação
        comentarios = Comentario.query.filter_by(id_post=post_id).order_by(Comentario.data_criacao.desc()).paginate(
            page=args['page'], per_page=args['limit'], error_out=False)

        # Formata os comentários para incluir informações do usuário
        comentarios_formatados = []
        for comentario in comentarios.items:
            usuario = Usuario.query.get(comentario.id_usuario)
            comentarios_formatados.append({
                "id": comentario.id,
                "conteudo": comentario.conteudo,
                "data_criacao": comentario.data_criacao.isoformat(),
                "usuario": {
                    "id": usuario.id,
                    "username": usuario.username
                }
            })

        return {
            "comentarios": comentarios_formatados,
            "total": comentarios.total,
            "page": comentarios.page,
            "pages": comentarios.pages
        }, 200


class CreateComentarioResource(Resource):
    @jwt_required()
    def post(self, post_id):
        user_id = get_jwt_identity()
        usuario = Usuario.query.get(user_id)
        post = Post.query.get(post_id)

        if not usuario:
            return {"error": "Usuário não encontrado"}, 404

        if not post:
            return {"error": "Post não encontrado"}, 404

        # Configura o parser para receber o conteúdo do comentário
        parser = reqparse.RequestParser()
        parser.add_argument('conteudo', type=str, required=True,
                            help="Conteúdo do comentário é obrigatório")
        args = parser.parse_args()

        # Cria o novo comentário
        novo_comentario = Comentario(
            conteudo=args['conteudo'],
            id_usuario=user_id,
            id_post=post_id,
            data_criacao=datetime.now()
        )

        db.session.add(novo_comentario)
        db.session.commit()

        return {
            "message": "Comentário criado com sucesso",
            "comentario": {
                "id": novo_comentario.id,
                "conteudo": novo_comentario.conteudo,
                "data_criacao": novo_comentario.data_criacao.isoformat(),
                "usuario": {
                    "id": usuario.id,
                    "username": usuario.username
                }
            }
        }, 201
