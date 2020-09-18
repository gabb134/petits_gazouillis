from flask import render_template, flash,redirect,url_for
from app import app
from app.formulaires import FormulaireEtablirSession
from app.models import Utilisateur
from flask_login import current_user, login_user, logout_user
from flask import request
from werkzeug.urls import url_parse
from flask_login import login_required
#from app.formulaires import FormulaireEnregistrement
from app import db
#from PIL import Image, ImageDraw, ImageFront
import random
import base64 
from io import BytesIO

@app.route('/')
@app.route('/index')
@login_required
def index():   
    utilisateur =current_user
    publication = current_user.publication.all()
    #utilisateur = Utilisateur.query.all()
    return render_template('index.html', titrex='Accueil', utilisateur=utilisateur,publication=publication) 


@app.route('/etablir_session',methods=['GET','POST'])
def etablir_session():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    formulaire = FormulaireEtablirSession()
    if formulaire.validate_on_submit():
         utilisateur = Utilisateur.query.filter_by(nom=formulaire.nom.data).first()
         if utilisateur is None or not utilisateur.valider_mot_de_passe(formulaire.mot_de_passe.data):
             flash('Nom utilisateur ou mot de passe invalide(s)')
             return redirect(url_for('etablir_session'))
         login_user(utilisateur, remember=formulaire.se_souvenir_de_moi.data)
         next_page = request.args.get('next')
         if not next_page or url_parse(next_page).netloc != '':
             return redirect(url_for('index'))
         return redirect(next_page)
    return render_template('etablir_session.html', titre='Établir une session', formulaire=formulaire)  

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))