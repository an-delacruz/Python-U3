from flask import Flask,request,jsonify
from flask_cors import CORS
from encrypt import bcrypt
from flask_migrate import Migrate
from config import BaseConfig
from database import db
from models import User
from sqlalchemy import exc
from functools import wraps

app = Flask(__name__)
app.config.from_object(BaseConfig)
CORS(app)
bcrypt.init_app(app)
db.init_app(app)

migrate = Migrate()
migrate.init_app(app,db)


@app.route('/auth/registro',methods=['POST'])
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

@app.route('/auth/login',methods=['POST'])
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
        
def obtenerInfo(token):
    if token:
        resp = User.decode_auth_token(token)
        user = User.query.filter_by(id=resp).first()
        if user:
            usuario = {
                'status':'Exitoso',
                'data':{
                    'user_id':user.id,
                    'email':user.email,
                    'admin':user.admin,
                    'registered_on':user.registered_on
                }
            }
            return usuario
        else:
            return {'status':'Faliido'}

def tokenCheck(f):
    wraps(f)
    def verificar(*args,**kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            return jsonify({'mensaje': 'Token no encontrando'})
        try:
            info = obtenerInfo(token)
            print(info)
            if info['status'] == 'Fallido':
                return jsonify({'mensaje': 'Token invalido'})
        except:
            return jsonify({'mensaje': 'Token invalido'})
        
        return f(info['data'],*args,**kwargs)
    return verificar

@app.route('/usuarios',methods=['GET'])
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