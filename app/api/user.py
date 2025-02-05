from flask_restful import Resource, reqparse
from flask_login import login_required, current_user
from app.extensions import db
import re


class ProfileResource(Resource):
    @login_required
    def get(self):
        """Endpoint para obter o perfil do usuário atual."""
        if not current_user.is_authenticated:
            return {"error": "Usuário não autenticado"}, 401

        return {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email
        }, 200


class UpdateResource(Resource):
    @login_required
    def put(self):
        """Endpoint para atualizar informações do usuário."""
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=False, trim=True)
        parser.add_argument('email', type=str, required=False, trim=True)
        data = parser.parse_args()

        if not any([data.get('username'), data.get('email')]):
            return {"error": "Nenhum dado foi enviado para atualização"}, 400

        if data.get('username'):
            if len(data['username']) < 3:
                return {"error": "O nome de usuário deve ter pelo menos 3 caracteres"}, 400  # noqa: E501
            current_user.username = data['username']

        if data.get('email'):
            if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
                return {"error": "E-mail inválido"}, 400
            current_user.email = data['email']

        db.session.commit()

        return {
            "status": "success",
            "message": "Usuário atualizado com sucesso",
            "data": {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email
            }
        }, 200
