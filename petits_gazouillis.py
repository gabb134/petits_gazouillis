from app import app, db
from app.models import Utilisateur, Publication



@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'U': Utilisateur, 'P': Publication}

print('Demarrage petits gazouillis')    

@app.before_first_request
def initialisation():
    print('initialisation')
    