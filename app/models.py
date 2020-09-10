from datetime import datetime
from app import db

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), index=True, unique=True)
    courriel = db.Column(db.String(120), index=True, unique=True)
    mot_de_passe_hash = db.Column(db.String(128))

    Publication = db.relationship('Publication', backref='auteur', lazy='dynamic')


    def __repr__(self):
        return '<Utilisateur {}>'.format(self.nom)    

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    corps = db.Column(db.String(140))
    horodatage = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.corps)