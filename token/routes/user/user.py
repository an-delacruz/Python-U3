from flask import Blueprint, request, jsonify
from sqlalchemy import exc
from models import User
from app import db, bcrypt
from auth import tokenCheck

appuser = Blueprint('appuser',__name__,template_folder='templates')

@appuser.route('/auth/registro',methods=['POST'])
def registro():
    user = request.get_json()
    userExists = User.query.filter_by(email=user['email']).first()
    if not userExists:
        usuario = User(user['email'],user['password'])
        try:
            db.session.add(usuario)
            db.session.commit()
            msg = "Usuario registrado correctamente"
        except exc.SQLAlchemyError as e:
            msg = "Error al registrar usuario"
    else:
        msg = "El usuario ya existe"
    return jsonify({'msg':msg})

@appuser.route('/auth/login',methods=['POST'])
def login():
    user = request.get_json()
    usuario = User(email=user['email'],password=user['password'])
    searchUser =  User.query.filter_by(email=usuario.email).first()
    if searchUser:
        validation = bcrypt.check_password_hash(searchUser.password,user['password'])
        if validation:
            auth_token = usuario.enconde_auto_token(user_id=searchUser.id)
            responseObj = {
                'status':'exitoso',
                'mensaje':'Login',
                'auth_token':auth_token
            }
            return jsonify(responseObj)
    return jsonify({'mensaje':'Datos incorrectos'})
        

@appuser.route('/usuarios',methods=['GET'])
@tokenCheck
def getUser(usuario):
    if usuario['admin']:
        output=[]
        usuarios = User.query.all()
        for user in usuarios:
            obj = {
                'id':user.id,
                'email':user.email,
                'password':user.password,
                'registered_on':user.registered_on,
                'admin':user.admin
            }
            output.append(obj)
        return jsonify({
            'status':'Exitoso',
            'data':output
        })