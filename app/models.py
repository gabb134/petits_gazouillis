from datetime import datetime
from app import db
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import etablir_session

@etablir_session.user_loader
def load_utilisateur(id):
    return Utilisateur.query.get(int(id))

partisans = db.Table('partisans',
    db.Column('partisans_id',db.Integer,db.ForeignKey('utilisateur.id')),
    db.Column('utilisateur_qui_est_suivi_id',db.Integer,db.ForeignKey('utilisateur.id'))
)

class Utilisateur(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), index=True, unique=True)
    courriel = db.Column(db.String(120), index=True, unique=True)
    mot_de_passe_hash = db.Column(db.String(128))
    avatar = db.Column(db.Text(131072), index =False, unique=False)
    a_propos_de_moi = db.Column(db.String(140))

    dernier_acces = db.Column(db.DateTime, default= datetime.utcnow)

    publication = db.relationship('Publication', backref='auteur', lazy='dynamic')

    les_partisans = db.relationship(
        'Utilisateur',secondary=partisans,
        primaryjoin=(partisans.c.partisans_id==id),
        secondaryjoin=(partisans.c.utilisateur_qui_est_suivi_id==id),
        backref = db.backref('partisans',lazy='dynamic'),lazy='dynamic')

    def devenir_partisan(self,utilisateur):
        if not self.est_partisan(utilisateur):
            print("ajouter partisans:{}".format(utilisateur.nom))
            self.les_partisans.append(utilisateur)
    
    def ne_plus_etre_partisan(self,utilisateur):
        if self.est_partisan(utilisateur):
            print("retirer partisan:{}".format(utilisateur.nom))
            self.les_partisans.remove(utilisateur)

    def est_partisan(self,utilisateur):
        return self.les_partisans.filter(
            partisans.c.utilisateur_qui_est_suivi_id == utilisateur.id).count() > 0     

    def Liste_publications_dont_je_suis_partisans(self):
        publication_suivies = Publication.query.join(
            partisans, (partisans.c.utilisateur_qui_est_suivi_id == Publication.utilisateur_id)).filter(
                partisans.c.partisans_id==self.id)
        mes_publications = Publication.query.filter_by(utilisateur_id = self.id)
        return mes_publications.union(publication_suivies).order_by(Publication.horodatage.desc())
        

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

        u = Utilisateur(nom=nom, courriel=courriel,avatar =avatar, a_propos_de_moi= a_propos_de_moi, dernier_acces=datetime.utcnow())
        u.enregistrer_mot_de_passe(mot_de_passe=mot_de_passe)

        return u
    
    return None
         