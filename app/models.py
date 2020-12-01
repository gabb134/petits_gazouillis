import base64
from datetime import datetime,timedelta
from app import db
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import etablir_session
from flask import url_for

@etablir_session.user_loader
def load_utilisateur(id):
    return Utilisateur.query.get(int(id))

partisans = db.Table('partisans',
    db.Column('partisans_id',db.Integer,db.ForeignKey('utilisateur.id')),
    db.Column('utilisateur_qui_est_suivi_id',db.Integer,db.ForeignKey('utilisateur.id'))
)
class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'suivant': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'precedent': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

class Utilisateur(PaginatedAPIMixin,UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), index=True, unique=True)
    courriel = db.Column(db.String(120), index=True, unique=True)
    mot_de_passe_hash = db.Column(db.String(128))
    avatar = db.Column(db.Text(131072), index =False, unique=False)
    a_propos_de_moi = db.Column(db.String(140))

    dernier_acces = db.Column(db.DateTime, default= datetime.utcnow)

    jeton = db.Column(db.String(32),index=True,unique=True)
    jeton_expiration = db.Column(db.DateTime)

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

    def to_dict(self):
        publications = self.Liste_publications_dont_je_suis_partisans()
        partisans = self.les_partisans

        data = {
            'id':self.id,
            'nom':self.nom,
            'courriel':self.courriel,
            'avatar': self.avatar,
            'a_propos_de_moi': self.a_propos_de_moi,
            'dernier_acces': self.dernier_acces,
            'publications':[item.id for item in publications], 
            'partisans': [item.id for item in partisans]
        }
        return data

    def to_dict_pour_jeton(self):
        publications = self.Liste_publications_dont_je_suis_partisans()
        partisans = self.les_partisans

        data =   { 'utilisateur':{ 
            'id':self.id,
            'nom':self.nom,
            'courriel':self.courriel,
            'avatar': self.avatar,
            'a_propos_de_moi': self.a_propos_de_moi,
            'dernier_acces': self.dernier_acces,
            'publications':[item.id for item in publications], 
            'partisans': [item.id for item in partisans]
        }}
        return data


    def __repr__(self):
        return '<Utilisateur {}>'.format(self.nom)  

    def enregistrer_mot_de_passe(self, mot_de_passe):
        self.mot_de_passe_hash = generate_password_hash(mot_de_passe)

    def valider_mot_de_passe(self, mot_de_passe):
        return check_password_hash(self.mot_de_passe_hash, mot_de_passe)

    def get_jeton(self, expire_dans = 3600):  
        maintenant = datetime.utcnow()
        if self.jeton and self.jeton_expiration > maintenant + timedelta(seconds=60):
            return self.jeton
        self.jeton = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.jeton_expiration = maintenant + timedelta(seconds=expire_dans)
        filtre = [';',':','!',"*","/"]
        for c in filtre:
            self.jeton = self.jeton.replace(c,'X')
        db.session.add(self)
        return self.jeton

    def revoquer_jeton(self):
        self.jeton_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def verifier_jeton(jeton):
        utilisateur = Utilisateur.query.filter_by(jeton=jeton).first()
        if utilisateur is None or utilisateur.jeton_expiration < datetime.utcnow():
            return None
        return utilisateur


class Publication(PaginatedAPIMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    corps = db.Column(db.String(140))
    horodatage = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.corps)
    def to_dict(self):
        data = {
            'id':self.id,
            'corps':self.corps,
            'horodatage':self.horodatage.isoformat() + 'Z',
            'utilisateur_id': self.utilisateur_id
        }
        return data


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
         