from flask import Blueprint, render_template, jsonify, request
from app.models import Usuario
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.forms import FormLogin, FormCriarConta

routes = Blueprint('routes', __name__)  # Definição do Blueprint


@routes.route('/', methods=["GET"])
def homepage():
    """Renderiza a página inicial com o formulário de login."""
    form = FormLogin()  # Instancia o formulário de login
    return render_template('homepage.html', form=form)


@routes.route('/criar-conta', methods=["GET"])
def criarconta():
    """Renderiza a página de criação de conta ."""
    form = FormCriarConta()  # Instancia o formulário de criação de conta
    return render_template('criarconta.html', form=form)


@routes.route('/feed', methods=["GET"])
def feed():
    return render_template('feed.html')


@routes.route('/perfil', methods=["GET"])
@jwt_required()
def perfil():
    """Protege, garantindo que o usuário esteja autenticado."""
    print(f"Headers recebidos: {request.headers}")  # Depuração no terminal
    user_id = get_jwt_identity()  # Obtém o ID do usuário a partir do token
    print(f"Usuário autenticado: {user_id}")  # Depuração no terminal
    usuario = Usuario.query.get(user_id)

    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    return render_template("perfil.html", usuario=usuario)


'''

from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask_login import login_required, login_user, current_user
from app.forms import FormLogin, FormCriarConta, FormFoto
from app.models import Usuario, Foto
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db, bcrypt
import os
from werkzeug.utils import secure_filename

routes = Blueprint('routes', __name__)  # Definição do Blueprint


@routes.route('/', methods=["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):  # noqa: E501
            login_user(usuario)
            return redirect(url_for("routes.perfil", id_usuario=usuario.id))
    return render_template('homepage.html', form=formlogin)


@routes.route('/criar-conta', methods=["GET", "POST"])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data, senha=senha, email=formcriarconta.email.data)  # noqa: E501
        db.session.add(usuario)
        db.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("routes.perfil", id_usuario=usuario.id))
    return render_template('criarconta.html', form=formcriarconta)


@routes.route('/perfil/<id_usuario>', methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        formfoto = FormFoto()
        fotos = Foto.query.filter_by(id_usuario=current_user.id).order_by(Foto.data_criacao.desc(), Foto.id.desc()).all()  # noqa: E501
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            nome_arquivo = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(
                os.path.dirname(__file__)), "uploads", nome_arquivo)
            arquivo.save(caminho)
            foto = Foto(imagem=nome_arquivo, id_usuario=current_user.id)
            db.session.add(foto)
            db.session.commit()
        return render_template("perfil.html", usuario=current_user, form=formfoto, fotos=fotos)  # noqa: E501
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)
'''

'''from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import FormLogin, FormCriarConta, FormFoto
from app.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename

@app.route('/', methods=["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):  # noqa: E501
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template('homepage.html', form=formlogin)

@app.route('/criar-conta', methods=["GET", "POST"])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data, senha=senha, email=formcriarconta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template('criarconta.html', form=formcriarconta)

@app.route('/perfil/<id_usuario>', methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        formfoto = FormFoto()
        fotos = Foto.query.filter_by(id_usuario=current_user.id).order_by(Foto.data_criacao.desc(), Foto.id.desc()).all()  # noqa: E501
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            nome_arquivo = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_arquivo)  # noqa: E501
            arquivo.save(caminho)
            foto = Foto(imagem=nome_arquivo, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=formfoto, fotos=fotos)  # noqa: E501
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)


'''
"""from flask import render_template, url_for, redirect
from werkzeug.utils import secure_filename

from app import app, bcrypt, database
from app.forms import FormLogin, FormCriarConta, FormFoto
from flask_login import login_required, login_user, logout_user, current_user
from app.models import Usuario, Foto
import os


@app.route('/', methods = [ "GET", "POST" ] )

def homepage():
    formlogin = FormLogin()

    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by( email = formlogin.email.data ).first()  # noqa: E501
        if usuario and bcrypt.check_password_hash( usuario.senha, formlogin.senha.data ):  # noqa: E501
            login_user( usuario )

            return redirect(url_for("perfil", id_usuario=usuario.id))

    return render_template( 'homepage.html', form = formlogin )

@app.route('/criar-conta', methods = [ "GET", "POST" ] )
def criarconta():
    formcriarconta = FormCriarConta()

    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash( formcriarconta.senha.data )
        usuario = Usuario( username = formcriarconta.username.data, senha = senha, email = formcriarconta.email.data )  # noqa: E501
        database.session.add( usuario )
        database.session.commit()

        login_user( usuario, remember = True )
        print("Usuário criado com sucesso. Redirecionando para perfil.")
        return redirect(url_for("perfil", id_usuario = usuario.id ) )

    print("Formulário de criação de conta não validado. Exibindo formulário novamente.")  # noqa: E501
    return render_template( 'criarconta.html', form = formcriarconta )

@app.route( '/logout' )
@login_required
def logout():
    logout_user()
    return redirect( url_for( "homepage" ) )

@app.route( '/feed' )
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc(), Foto.id.desc()).all()
    return render_template( "feed.html", fotos = fotos )

@app.route('/perfil/<id_usuario>', methods=["GET", "POST"])
@login_required
def perfil( id_usuario ):

    if int( id_usuario ) == int( current_user.id ):
        formfoto = FormFoto()
        fotos = Foto.query.filter_by(id_usuario=current_user.id).order_by(Foto.data_criacao.desc(), Foto.id.desc()).all()  # noqa: E501
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            nome_arquivo = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_arquivo )  # noqa: E501

            arquivo.save( caminho )

            foto = Foto( imagem = nome_arquivo, id_usuario = current_user.id )
            database.session.add( foto )
            database.session.commit()

        return render_template( "perfil.html", usuario = current_user, form = formfoto, fotos=fotos )  # noqa: E501
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)"""
