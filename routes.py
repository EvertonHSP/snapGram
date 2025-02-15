from flask import Blueprint, render_template, jsonify, request
from app.models import Usuario
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.forms import FormLogin, FormCriarConta

routes = Blueprint('routes', __name__)


@routes.route('/', methods=["GET"])
@routes.route('/homepage', methods=["GET"])
def homepage():

    form = FormLogin()
    #return render_template('homepage.html', form=form)


@routes.route('/criar-conta', methods=["GET"])
def criarconta():

    form = FormCriarConta()
    #return render_template('criarconta.html', form=form)


@routes.route('/feed', methods=["GET"])
def feed():
    #return render_template('feed.html')


@routes.route('/perfil', methods=["GET"])
@jwt_required()
def perfil():
    print(f"Headers recebidos: {request.headers}")
    user_id = get_jwt_identity()
    print(f"Usuário autenticado: {user_id}")
    usuario = Usuario.query.get(user_id)

    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    #return render_template("perfil.html", usuario=usuario)
