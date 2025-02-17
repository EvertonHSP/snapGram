import os
from datetime import datetime
from flask import request
from werkzeug.utils import secure_filename
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Post, Usuario
# Configurações para o upload de imagens
UPLOAD_FOLDER = 'uploads/fotos_posts'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

        if 'foto' not in request.files:
            return {"error": "Nenhum arquivo de imagem enviado"}, 400

        file = request.files['foto']

        if file.filename == '':
            return {"error": "Nome do arquivo inválido"}, 400

        if file and allowed_file(file.filename):
            # Obtém a extensão do arquivo
            ext = file.filename.rsplit('.', 1)[1].lower()

            # Obtém a legenda
            legenda = request.form.get('legenda')
            if not legenda:
                return {"error": "Legenda é obrigatória"}, 400

            # Cria um novo post com um valor temporário para imagem
            novo_post = Post(
                legenda=legenda,
                imagem="temp.jpg",  # Valor temporário
                id_usuario=user_id,
                data_criacao=datetime.now()
            )

            db.session.add(novo_post)
            db.session.commit()  # Agora novo_post.id existe

            # Define o nome final do arquivo
            filename = f"{user_id}_{novo_post.id}.{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Atualiza o caminho correto da imagem
            novo_post.imagem = filepath
            db.session.commit()

            return {
                "message": "Post criado com sucesso",
                "post": {
                    "id": novo_post.id,
                    "legenda": novo_post.legenda,
                    "imagem": novo_post.imagem,
                    "data_criacao": novo_post.data_criacao.isoformat(),
                    "id_usuario": novo_post.id_usuario
                }
            }, 201
        else:
            return {"error": "Tipo de arquivo não permitido"}, 400
