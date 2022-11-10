class BaseConfig:
    USER_DB ='postgres'
    PASS_DB = 'admin'
    URL_DB = 'localhost'
    NAME_BD = 'clase_login'
    FULL_URL = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_BD}'
    SQLALCHEMY_DATABASE_URI = FULL_URL
    SECRET_KEY = 'secretKEY123'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False