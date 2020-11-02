from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPTokenAuth

from app.models import Utilisateur
from app.api.erreurs import reponse_erreur_json

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    print("Nom{} Mot de passe{}".format(username, password))
    utilisateur = Utilisateur.query.filter_by(nom=username).first()
    if utilisateur and utilisateur.valider_mot_de_passe(password):
        return utilisateur

@basic_auth.error_handler
def basic_auth_error(status):
    return reponse_erreur_json(status,"Erreur authentification")

@token_auth.verify_token
def verify_token(token):
    return Utilisateur.verifier_jeton(token) if token else None

@token_auth.error_handler
def token_auth_error(status):
    return reponse_erreur_json(status)  

