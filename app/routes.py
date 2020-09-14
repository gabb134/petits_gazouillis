from flask import render_template, flash,redirect,url_for
from app import app
from app.formulaires import FormulaireEtablirSession
from app.models import Utilisateur

@app.route('/')
@app.route('/index')
def index():

    utilisateur = Utilisateur.query.all()

    return render_template('index.html', titrex='Accueil', utilisateur=utilisateur) 


@app.route('/etablir_session',methods=['GET','POST'])
def etablir_session():
    formulaire = FormulaireEtablirSession()
    if formulaire.validate_on_submit():
        flash('Établir une session par utilisateur {}, se_souvenir_de_moi ={}'.format(formulaire.nom.data, formulaire.se_souvenir_de_moi.data))
        return redirect( url_for('index') )
    return render_template('etablir_session.html', titre='Établir une session', formulaire=formulaire)  