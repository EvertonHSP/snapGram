from sqlalchemy.exc import IntegrityError
import os
from flask import request, Flask, url_for
from werkzeug.utils import secure_filename
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.extensions import db
from app.models import Post, Usuario, Curtida, TokenBlacklist


class PostLikesResource(Resource):
    def get(self, post_id):
        
        post = Post.query.get(post_id)
        if not post:
            return {"error": "Post não encontrado"}, 404

        
        curtidas = Curtida.query.filter_by(id_post=post_id).all()

        usuarios_curtiu = []
        for curtida in curtidas:
            usuario = Usuario.query.get(curtida.id_usuario)
            if usuario:
                usuarios_curtiu.append({
                    "id": usuario.id,
                    "username": usuario.username
                })

        
        return {
            "post_id": post_id,
            "total_curtidas": len(curtidas),
            "usuarios_curtiu": usuarios_curtiu
        }, 200


class CurtirPostResource(Resource):
    @jwt_required()  
    def post(self, post_id):
        blacklist_check = check_token_blacklist()
        if blacklist_check:
            return blacklist_check
        
        user_id = get_jwt_identity()

        post = Post.query.get(post_id)
        if not post:
            return {"error": "Post não encontrado"}, 404

        
        curtida_existente = Curtida.query.filter_by(
            id_post=post_id, id_usuario=user_id).first()
        if curtida_existente:
            return {"message": "Você já curtiu este post"}, 400

        
        nova_curtida = Curtida(id_usuario=user_id, id_post=post_id)

        try:
            
            db.session.add(nova_curtida)
            db.session.commit()
            return {"message": "Post curtido com sucesso"}, 201
        except IntegrityError:
            
            db.session.rollback()
            return {"error": "Erro ao curtir o post: você já curtiu este post."}, 400
        except Exception as e:
            
            db.session.rollback()
            return {"error": f"Erro inesperado: {str(e)}"}, 500

    @jwt_required()  
    def delete(self, post_id):
        blacklist_check = check_token_blacklist()
        if blacklist_check:
            return blacklist_check
       
        user_id = get_jwt_identity()

        
        post = Post.query.get(post_id)
        if not post:
            return {"error": "Post não encontrado"}, 404

        
        curtida_existente = Curtida.query.filter_by(
            id_post=post_id, id_usuario=user_id).first()
        if not curtida_existente:
            return {"message": "Você ainda não curtiu este post"}, 400

        try:
            
            db.session.delete(curtida_existente)
            db.session.commit()
            return {"message": "Curtida removida com sucesso"}, 200
        except Exception as e:
            
            db.session.rollback()
            return {"error": f"Erro inesperado: {str(e)}"}, 500



def check_token_blacklist():
    decoded_token = get_jwt()
    jti = decoded_token["jti"]
    if TokenBlacklist.query.filter_by(token=jti).first():
        return {"error": "Token inválido. Faça login novamente."}, 401
    return None