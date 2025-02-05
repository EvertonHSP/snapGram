from flask_restful import Resource, reqparse
from flask_login import logout_user
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required  # noqa: E501
from app import bcrypt  # database
from app.models import Usuario, TokenBlacklist
from app.extensions import db


class RegisterResource(Resource):
    def post(self):
        """Endpoint para registrar um novo usuário e retornar um token JWT."""
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

        # Criar um token JWT após o registro
        access_token = generate_unique_token(novo_usuario.id)
        return {"message": "Usuário criado com sucesso!", "access_token": access_token}, 201  # noqa: E501


class LoginResource(Resource):
    def post(self):
        """Faz login e retorna um token JWT"""
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True,
                            help="Email é obrigatório")
        parser.add_argument('password', type=str,
                            required=True, help="Senha é obrigatória")
        data = parser.parse_args()

        usuario = Usuario.query.filter_by(email=data['email']).first()
        if not usuario or not bcrypt.check_password_hash(usuario.senha, data["password"]):  # noqa: E501
            return {"error": "Credenciais inválidas"}, 401

        # Criar um token JWT
        access_token = generate_unique_token(usuario.id)
        return {"message": "Login realizado!", "access_token": access_token}, 200  # noqa: E501


class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        """Endpoint para realizar o logout."""
        # Pegar o ID do usuário do token JWT
        # O `get_jwt_identity` já retorna o ID do usuário.
        usuario_id = get_jwt_identity()

        # Verificar se o usuário já tem um token na blacklist
        existing_token = TokenBlacklist.query.filter_by(
            user_id=usuario_id).first()
        if existing_token:
            # Se o token já existir na blacklist, removê-lo
            db.session.delete(existing_token)

        # Adicionar o token atual à blacklist
        blacklisted_token = TokenBlacklist(
            token=str(get_jwt_identity()), user_id=usuario_id)
        db.session.add(blacklisted_token)
        db.session.commit()

        logout_user()  # Desconectar o usuário
        return {"message": "Logout bem-sucedido"}, 200


def generate_unique_token(usuario_id):
    """Função para gerar um token único, que não seja igual ao token revogado."""   # noqa: E501
    while True:
        # Gerar um token com create_access_token
        token = create_access_token(identity=usuario_id)
        print(f"Token gerado: {token}")
        # Verificar se o token já existe na blacklist
        if TokenBlacklist.query.filter_by(token=token).first():
            # Se o token já estiver na blacklist, gerar outro
            continue
        else:
            # Se não estiver, retornar o token
            return token
