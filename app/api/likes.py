import os
from flask import request, Flask, url_for
from werkzeug.utils import secure_filename
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Post, Usuario, Curtida


class PostLikesResource(Resource):
    def get(self, post_id):
        # Busca o post pelo ID
        post = Post.query.get(post_id)
        if not post:
            return {"error": "Post não encontrado"}, 404

        # Obtém as curtidas do post
        curtidas = Curtida.query.filter_by(id_post=post_id).all()

        # Lista para armazenar os usuários que curtiram o post
        usuarios_curtiu = []
        for curtida in curtidas:
            usuario = Usuario.query.get(curtida.id_usuario)
            if usuario:
                usuarios_curtiu.append({
                    "id": usuario.id,
                    "username": usuario.username
                })

        # Retorna as curtidas do post
        return {
            "post_id": post_id,
            "total_curtidas": len(curtidas),
            "usuarios_curtiu": usuarios_curtiu
        }, 200


class CurtirPostResource(Resource):
    @jwt_required()  # Requer autenticação JWT
    def post(self, post_id):
        # Obtém o ID do usuário logado
        user_id = get_jwt_identity()

        # Verifica se o post existe
        post = Post.query.get(post_id)
        if not post:
            return {"error": "Post não encontrado"}, 404

        # Verifica se o usuário já curtiu o post
        curtida_existente = Curtida.query.filter_by(
            id_post=post_id, id_usuario=user_id).first()
        if curtida_existente:
            return {"message": "Você já curtiu este post"}, 400

        # Cria uma nova curtida
        nova_curtida = Curtida(id_usuario=user_id, id_post=post_id)

        # Adiciona a nova curtida ao banco de dados
        db.session.add(nova_curtida)
        db.session.commit()

        return {"message": "Post curtido com sucesso"}, 201
