from models import User
from functools import wraps
from flask import request,jsonify



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
