from datetime import datetime
from flask_login import UserMixin
from marshmallow import Schema, fields
from app.extensions import db


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False,
                         unique=True, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    fotos = db.relationship('Foto', backref='usuario',
                            lazy=True, cascade="all, delete")
    posts = db.relationship('Post', backref='usuario',
                            lazy=True, cascade="all, delete")
    comentarios = db.relationship(
        'Comentario', backref='usuario', lazy=True, cascade="all, delete")
    curtidas = db.relationship(
        'Curtida', backref='usuario', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"<Usuario {self.username}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = db.Column(db.Integer, db.ForeignKey(
        'usuario.id', ondelete="CASCADE"), nullable=False)

    comentarios = db.relationship(
        'Comentario', backref='post', lazy=True, cascade="all, delete")
    curtidas = db.relationship(
        'Curtida', backref='post', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"<Post {self.id} - {self.titulo}>"


class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = db.Column(db.Integer, db.ForeignKey(
        'usuario.id', ondelete="CASCADE"), nullable=False)
    id_post = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"<Comentario {self.id}>"


class Foto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String, default='default.jpg')
    data_criacao = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = db.Column(db.Integer, db.ForeignKey(
        'usuario.id'), nullable=False)


class Curtida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey(
        'usuario.id', ondelete="CASCADE"), nullable=False)
    id_post = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"<Curtida {self.id}>"


class PostSchema(Schema):
    id = fields.Int()
    titulo = fields.Str()
    conteudo = fields.Str()
    data_criacao = fields.DateTime()
    id_usuario = fields.Int()


class ComentarioSchema(Schema):
    id = fields.Int()
    conteudo = fields.Str()
    data_criacao = fields.DateTime()
    id_usuario = fields.Int()
    id_post = fields.Int()


class CurtidaSchema(Schema):
    id = fields.Int()
    id_usuario = fields.Int()
    id_post = fields.Int()


class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'usuario.id'), nullable=False)  # Chave estrangeira
    usuario = db.relationship('Usuario', backref=db.backref(
        'blacklisted_tokens', lazy=True))  # Relacionamento com o usuário

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id
