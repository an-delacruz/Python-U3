from flask import Flask,request,jsonify
from flask_cors import CORS
from encrypt import bcrypt
from flask_migrate import Migrate
from config import BaseConfig
from database import db
from models import User
from sqlalchemy import exc
from functools import wraps
from routes.user.user import appuser

app = Flask(__name__)
app.register_blueprint(appuser)
app.config.from_object(BaseConfig)
CORS(app)
bcrypt.init_app(app)
db.init_app(app)

migrate = Migrate()
migrate.init_app(app,db)

