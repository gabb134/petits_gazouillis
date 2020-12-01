from app.api import bp
from app.models import Utilisateur
from flask import jsonify
from flask import request 
from flask_cors import cross_origin
from app.api.auth import basic_auth
from app.api.auth import token_auth 


@bp.route('/utilisateurs2',methods=['GET'])
def get_utilisateurs2():
    return 'utilisateurs2'


#CRUD  Create, Read, Update, Delete

#Lire une publication
@bp.route('/utilisateurs/<int:id>', methods=['GET'])
@cross_origin()
@token_auth.login_required
def get_utilisateur(id):
    return jsonify(Utilisateur.query.get_or_404(id).to_dict())

#Lire toutes les publications
@bp.route('/utilisateurs',methods=['GET'])
@cross_origin()
@token_auth.login_required
def get_utilisateurss():
    page = request.args.get('page',1,type=int)
    par_page = min(request.args.get('par_page',10,type=int),100)
    data = Utilisateur.to_collection_dict(Utilisateur.query,page,par_page,'api.get_publications')
    return jsonify(data)




#creer
@bp.route('/utilisateurs',methods=['POST'])
def creer_utilisateur():
    return "creer"

#modifier
@bp.route('/utilisateurs/<int:id>', methods=['PUT'])
def modifier_utilisateur(id):
    return "modifier"

#supprimer
@bp.route('/utilisateurs/<int:id>', methods=['DELETE'])
def supprimer_utilisateur(id):
    return "supprimer"


