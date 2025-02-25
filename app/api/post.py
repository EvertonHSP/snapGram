import os
from datetime import datetime
from flask import request, Flask, url_for
from werkzeug.utils import secure_filename
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Usuario, Foto, Post

# Configurações para o upload de imagens de perfil
UPLOAD_FOLDER_PERFIL = 'uploads/fotos_perfil'
UPLOAD_FOLDER = 'uploads/fotos_posts'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER_PERFIL):
    os.makedirs(UPLOAD_FOLDER_PERFIL)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class PostListResource(Resource):
    def get(self):
        # Debug: Verifica se a função está sendo chamada
        print("Entrou na função get()")

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1,
                            location='args')  # Parâmetro de consulta
        parser.add_argument('limit', type=int, default=10,
                            location='args')  # Parâmetro de consulta
        parser.add_argument('user_id', type=int, required=False,
                            location='args')  # Parâmetro de consulta
        args = parser.parse_args()  # Extrai os parâmetros da requisição

        query = Post.query
        if args['user_id']:
            # Filtra posts por ID do usuário
            query = query.filter_by(id_usuario=args['user_id'])

        # Paginação dos posts
        posts = query.order_by(Post.data_criacao.desc()).paginate(
            page=args['page'], per_page=args['limit'], error_out=False)

        # Formata os dados para incluir a URL da imagem, o ID do usuário, a URL da foto de perfil e outras informações
        fotos = []
        for post in posts.items:
            usuario = Usuario.query.get(post.id_usuario)
            imagem_url = url_for(
                'upload.uploaded_file', filename=post.imagem.split('\\')[-1], _external=True)

            # Busca a foto de perfil do usuário
            foto_perfil = Foto.query.filter_by(id_usuario=usuario.id).first()
            foto_perfil_url = None
            if foto_perfil:
                foto_perfil_url = url_for(
                    'upload.uploaded_file_perfil', filename=foto_perfil.imagem.split('\\')[-1], _external=True)

            fotos.append({
                "id": post.id,  # ID do post
                "imagem_url": imagem_url,  # URL completa da imagem do post
                "data_criacao": post.data_criacao.isoformat(),  # Data de criação formatada
                "legenda": post.legenda,  # Legenda do post
                "usuario": {
                    "id": usuario.id,  # ID do usuário
                    "username": usuario.username,  # Nome de usuário
                    "foto_perfil_url": foto_perfil_url  # URL da foto de perfil do usuário
                }
            })

        return {
            "fotos": fotos,  # Lista de posts formatados
            "total": posts.total,  # Total de posts
            "page": posts.page,  # Página atual
            "pages": posts.pages  # Total de páginas
        }, 200


class PostResource(Resource):
    def get(self, post_id):
        # Busca o post pelo ID
        post = Post.query.get(post_id)
        if not post:
            return {"error": "Post não encontrado"}, 404

        # Busca o usuário associado ao post
        usuario = Usuario.query.get(post.id_usuario)
        if not usuario:
            return {"error": "Usuário associado ao post não encontrado"}, 404

        # Gera a URL da imagem
        imagem_url = url_for(
            'upload.uploaded_file', filename=post.imagem.split('\\')[-1], _external=True)
     # Busca a foto de perfil do usuário
        foto_perfil = Foto.query.filter_by(id_usuario=usuario.id).first()
        foto_perfil_url = None
        if foto_perfil:
            foto_perfil_url = url_for(
                'upload.uploaded_file_perfil', filename=foto_perfil.imagem.split('\\')[-1], _external=True)

        # Retorna os dados do post formatados
        return {
            "id": post.id,
            "imagem_url": imagem_url,
            "data_criacao": post.data_criacao.isoformat(),
            "legenda": post.legenda,
            "usuario": {
                "id": usuario.id,
                "username": usuario.username,
                "foto_perfil_url": foto_perfil_url
            }
        }, 200


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


class DeletePostResource(Resource):
    @jwt_required()  # Requer autenticação JWT
    def delete(self, post_id):
        # Obtém o ID do usuário logado a partir do token JWT
        user_id = int(get_jwt_identity())

        # Busca o post pelo ID
        post = Post.query.get(post_id)
        if not post:
            return {"error": "Post não encontrado"}, 404

        # Verifica se o usuário logado é o proprietário do post
        if post.id_usuario != user_id:
            return {"error": "Você não tem permissão para excluir este post"}, 403

        try:
            # Remove o arquivo de imagem associado ao post
            if os.path.exists(post.imagem):
                os.remove(post.imagem)

            # Remove o post do banco de dados
            db.session.delete(post)
            db.session.commit()

            return {"message": "Post excluído com sucesso"}, 200
        except Exception as e:
            db.session.rollback()  # Desfaz a transação em caso de erro
            return {"error": f"Erro ao excluir o post: {str(e)}"}, 500


class UploadFotoPerfilResource(Resource):
    @jwt_required()
    def post(self):
        # Obtém o ID do usuário logado a partir do token JWT
        user_id = get_jwt_identity()
        usuario = Usuario.query.get(user_id)
        print("user_id, usuario:  ", user_id, usuario)
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

            # Define o nome final do arquivo
            filename = f"{user_id}_perfil.{ext}"
            filepath = os.path.join(UPLOAD_FOLDER_PERFIL, filename)

            # Salva o arquivo no sistema de arquivos
            file.save(filepath)

            # Cria ou atualiza a foto de perfil do usuário
            foto_perfil = Foto.query.filter_by(id_usuario=user_id).first()
            if foto_perfil:
                # Atualiza a foto de perfil existente
                foto_perfil.imagem = filepath
                foto_perfil.data_criacao = datetime.utcnow()
            else:
                # Cria uma nova foto de perfil
                foto_perfil = Foto(
                    imagem=filepath,
                    id_usuario=user_id,
                    data_criacao=datetime.utcnow()
                )
                db.session.add(foto_perfil)

            db.session.commit()

            return {
                "message": "Foto de perfil atualizada com sucesso",
                "foto_perfil": {
                    "id": foto_perfil.id,
                    "imagem": foto_perfil.imagem,
                    "data_criacao": foto_perfil.data_criacao.isoformat(),
                    "id_usuario": foto_perfil.id_usuario
                }
            }, 200
        else:
            return {"error": "Tipo de arquivo não permitido"}, 400


class FotoPerfilResource(Resource):
    def get(self, usuario_id):
        """
        Retorna a URL da foto de perfil do usuário com base no ID fornecido.
        """
        # Busca o usuário no banco de dados
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return {"error": "Usuário não encontrado"}, 404

        # Busca a foto de perfil do usuário
        foto_perfil = Foto.query.filter_by(id_usuario=usuario_id).first()
        if not foto_perfil:
            return {"error": "Foto de perfil não encontrada"}, 404

        # Gera a URL da imagem de perfil
        foto_perfil_url = url_for(
            'upload.uploaded_file_perfil', filename=foto_perfil.imagem.split('\\')[-1], _external=True)

        # Retorna a URL da foto de perfil
        return {
            "foto_perfil_url": foto_perfil_url
        }, 200
