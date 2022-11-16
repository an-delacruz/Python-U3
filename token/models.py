import jwt
import datetime
from config import BaseConfig
from app import db,bcrypt

class User(db.Model):
    __tableName__ = "users"
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(255),unique=True,nullable=True)
    password = db.Column(db.String(255),nullable=False)
    registered_on = db.Column(db.DateTime,nullable=False)
    admin = db.Column(db.Boolean,nullable=False)
    
    def __init__(self,email,password,admin=False) -> None:
        self.email = email
        self.password = bcrypt.generate_password_hash(password,BaseConfig.BCRYPT_LOG_ROUNDS).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin
    
    def enconde_auto_token(self,user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0,minutes=10),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                BaseConfig.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e
    
    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token,BaseConfig.SECRET_KEY,algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        


class Image(db.Model):
    __tablename = 'user_images'
    id_imagen = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(128),nullable=False)
    data = db.Column(db.LargeBinary,nullable=False)
    rendered_date = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    
    region = db.relationship('User',backref='users')
    