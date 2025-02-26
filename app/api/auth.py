from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt, decode_token  # noqa: E501
from app import bcrypt
from app.models import Usuario, TokenBlacklist
from app.extensions import db



class RegisterResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True,
                            help="Email é obrigatório")
        parser.add_argument('password', type=str,
                            required=True, help="Senha é obrigatória")
        parser.add_argument('username', type=str, required=True,
                            help="Nome de usuário é obrigatório")
        data = parser.parse_args()

        if Usuario.query.filter_by(email=data['email']).first():
            return {"error": "E-mail já registrado"}, 400

        senha_cripto = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')
        novo_usuario = Usuario(
            username=data['username'], email=data['email'], senha=senha_cripto)
        db.session.add(novo_usuario)
        db.session.commit()

        access_token = generate_unique_token(novo_usuario.id)
        return {"message": "Usuário criado com sucesso!", "access_token": access_token}, 201  # noqa: E501


class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True,
                            help="Email é obrigatório")
        parser.add_argument('password', type=str,
                            required=True, help="Senha é obrigatória")
        data = parser.parse_args()

        usuario = Usuario.query.filter_by(email=data['email']).first()
        if not usuario or not bcrypt.check_password_hash(usuario.senha, data["password"]):  # noqa: E501
            return {"error": "Credenciais inválidas"}, 401

        access_token = generate_unique_token(usuario.id)
        return {"message": "Login realizado!", "access_token": access_token}, 200  # noqa: E501


class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        usuario_id = get_jwt_identity()

        raw_token = get_jwt()["jti"]  

        
        existing_token = TokenBlacklist.query.filter_by(token=raw_token).first()
        if existing_token:
            db.session.delete(existing_token)

        
        blacklisted_token = TokenBlacklist(token=raw_token, user_id=usuario_id)
        db.session.add(blacklisted_token)
        db.session.commit()

        return {"message": "Logout bem-sucedido"}, 200



def generate_unique_token(usuario_id):
    from flask import current_app  
    
    while True:
        
        token = create_access_token(identity=str(usuario_id))

        decoded_token = decode_token(token)
        jti = decoded_token["jti"]  
        
        if TokenBlacklist.query.filter_by(token=jti).first():
            continue  
        else:
            return token  