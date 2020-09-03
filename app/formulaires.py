from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class FormulaireEtablirSession(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    se_souvenir_de_moi = BooleanField('Se souvenir de moi')
    soumettre = SubmitField('Etablir une session')