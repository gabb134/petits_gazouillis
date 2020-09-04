from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class FormulaireEtablirSession(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired(message="Nom est un champ obligatoire")])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired(message="Mot de passe est un champ obligatoire")])
    se_souvenir_de_moi = BooleanField('Se souvenir de moi')
    soumettre = SubmitField('Etablir une session')