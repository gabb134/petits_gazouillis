from datetime import datetime
from app import db
import os
from werkzeug.security import generate_password_hash, check_password_hash

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), index=True, unique=True)
    courriel = db.Column(db.String(120), index=True, unique=True)
    mot_de_passe_hash = db.Column(db.String(128))
    avatar = db.Column(db.Text(131072), index =False, unique=False)
    a_propos_de_moi = db.Column(db.String(140))

    Publication = db.relationship('Publication', backref='auteur', lazy='dynamic')
    

    def __repr__(self):
        return '<Utilisateur {}>'.format(self.nom)  

    def enregistrer_mot_de_passe(self, mot_de_passe):
        self.mot_de_passe_hash = generate_password_hash(mot_de_passe)

    def valider_mot_de_passe(self, mot_de_passe):
        return check_password_hash(self.mot_de_passe_hash, mot_de_passe)

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    corps = db.Column(db.String(140))
    horodatage = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.corps)


def get_modele(modele, ligne, racine):

    if modele == "publication":
        id = int(ligne[0])
        corps = ligne[1].strip()
        datheure = ligne[2].strip()

        horodatage = datetime.strptime(datheure,'%Y-%m-%d %H:%M:%S.%f')
        u = Utilisateur.query.get(id)

        p = Publication(corps=corps, utilisateur_id=id, horodatage=horodatage, auteur=u)
        print(id)
        print(u.nom)
        print(p.utilisateur_id)
        return p

    if modele == "utilisateur":
        nom = ligne[0].strip()
        courriel = ligne[1].strip()
        mot_de_passe = ligne[2].strip()
        a_propos_de_moi = ligne[3].strip()
        fichier = 'base64/' + nom + '.base64'
        source = os.path.join(racine, fichier)
        print(source)

        if os.path.isfile(source):
            with open(source,'r') as mon_avatar:
                avatar = mon_avatar.read()
        else:
            avatar = "PAS DÉFINI"

        u = Utilisateur(nom=nom, courriel=courriel,avatar =avatar, a_propos_de_moi= a_propos_de_moi)
        u.enregistrer_mot_de_passe(mot_de_passe=mot_de_passe)

        return u
    
    return None
         