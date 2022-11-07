from flask import Flask,request,jsonify
from flask_cors import CORS
from encrypt import bcrypt
from flask_migrate import Migrate
from config import BaseConfig
from database import db

app = Flask(__name__)
app.config.from_object(BaseConfig)
CORS(app)
bcrypt.init_app(app)
db.init_app(app)

migrate = Migrate()
migrate.init_app(app,db)