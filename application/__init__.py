from flask import Flask
from flask_pymongo import PyMongo

app= Flask(__name__)
app.secret_key = '5A5A5B5B5C5C5D5D5E5E5F5F60616263'


app.config['UPLOAD_FOLDER'] ="C:/Users/HP/Documents/PFE/fichierTelecharger"


app.config["MONGO_URI"]="mongodb://localhost:27017/Seismos"
mongodb_client =PyMongo(app)
db = mongodb_client.db

from application.routes import main
from application.routes import auth
from application.routes import acceuil
from application.routes import ajouterMission
from application.routes import map
from application.routes import ajouterMissionPost
from application.routes import Ajouter_rapport
from application.routes import ajouterMateriel
from application.routes import consulter_mission
from application.routes import consulter_mission_info_affich
from application.routes import modifierMission
from application.routes import consulter_rapport
from application.routes import gererEquipe
from application.routes import creerCompte
from application.routes import MailAccord
from application.routes import gererMateriel
from application.routes import Ajouter_patient
from application.routes import modifier_patient
from application.routes import consulter_liste_patients
from application.routes import consulter_liste_decedes
from application.routes import Enregistrer_etude
from application.routes import Enregistrer_seisme
from application.routes import changer_mdp
from application.routes import Ajouter_deces
from application.routes import modifier_deces
from application.routes import consulter_liste_seisme
from application.routes import consulter_liste_etude
from application.routes import consulter_info_seisme
from application.routes import consulter_info_etude
from application.routes import modifier_seisme
from application.routes import modifier_etude
from application.routes import Enregistrer_intervenant
from application.routes import consulter_liste_intervenant