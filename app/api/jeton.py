from app.api import bp
from app import db
from flask import jsonify
from app.api.auth import basic_auth
from app.api.auth import token_auth


@bp.route('/jetons2',methods=['GET'])
def get_jetons2():
    return 'jetons2'

@bp.route('/jeton',methods=['GET'])
@basic_auth.login_required
def get_jeton():
    print('get_jeton')
    jeton = basic_auth.current_user().get_jeton()
    db.session.commit()
    return jsonify({'jeton': jeton})
     
@bp.route('/jeton',methods=['DELETE'])
@token_auth.login_required
def effacer_jeton():
    token_auth.current_user().revoquer_jeton()
    db.session.commit()
    return '',204