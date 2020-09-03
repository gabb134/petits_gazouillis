from flask import render_template
from app import app
from app.formulaires import FormulaireEtablirSession

@app.route('/')
@app.route('/index')
def index():
    abc = {"nom":"Monsieur Patate"}
    publications = [
        {
            'auteur': {'nom': 'John'},
            'corps': 'J\'aime les patates!!!'
        },
        {
            'auteur': {'nom': 'Jean'},
            'corps': 'Moi itou!!!'
        }
    ]
    return render_template('index.html', titrex='Accueil', utilisateur=abc,publications=publications) 


@app.route('/etablir_session')
def etablir_session():
    formulaire = FormulaireEtablirSession()
    return render_template('etablir_session.html', titre='Établir une session', formulaire=formulaire)  