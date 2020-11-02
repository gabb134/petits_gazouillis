from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from app import app
from flask import render_template, request
from app import db

def reponse_erreur_json(status_code, message=None):
    if message is not None:
        payload = {'erreur': message + " " + str(status_code)}
    else:
        payload = {'erreur': str(status_code) }
    print(payload)

    response = jsonify(payload)
    response.status_code = status_code
    return response

def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']

@app.errorhandler(404)
def bad_request(message):
    if wants_json_response():
        return reponse_erreur_json(400,"Requête invalide!")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(message):
    db.session.rollback()
    if wants_json_response():
        return reponse_erreur_json(500,"Erreur interne")
    return render_template('500.html'), 500