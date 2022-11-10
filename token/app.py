from flask import Flask,request,jsonify
from flask_cors import CORS
from encrypt import bcrypt
from flask_migrate import Migrate
from config import BaseConfig
from database import db
from models import User
from sqlalchemy import exc

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
        