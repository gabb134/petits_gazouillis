import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mon-mot-de-passe-tres-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'petits_gazouillis.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BD_TABLES_EFFACER = os.environ.get('BD_TABLES_EFFACER') or ['partisans','publication','utilisateur']
    BD_TABLES_CREER = os.environ.get('BD_TABLES_CREER') or ['utilisateur','publication']

    MAIL_SERVER= "localhost"
    MAIL_PORT= 8025
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') 
    MAIL_PASSWORD= os.environ.get('MAIL_PASSWORD') 
    ADMINS= ['cesarmarrero7@gmail.com']