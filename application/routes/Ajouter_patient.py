import base64
import re
from bson.binary import Binary
from application import app
from flask import Flask, Blueprint, render_template, request, session
from pymongo import MongoClient
from application import db
from application.routes.acceuil import verifierSession

@app.route("/formulaire_ajouter_patient")
def afficher_ajouter_patient():
    messages_erreur = {}
    info_patient={}
    
    idU = session['utilisateur_id']
    mission = db.affectation.find({ 'idmembre': idU})
    
    if verifierSession() == "Personnel médical Membre" :
        return render_template("personnel_medical.html" , poste ="Personnel médical Membre" ,messages_erreur=messages_erreur ,missions=mission , info_patient=info_patient )
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("personnel_medical.html" , poste ="Responsable de sécurité Membre" ,messages_erreur=messages_erreur ,missions=mission , info_patient=info_patient )
    
    
    
@app.route("/ajouter_patient" , methods=['POST'])
def ajouter_patient():
    idU = session['utilisateur_id'] 
    mission = db.affectation.find({ 'idmembre': idU})
    
    contraintes = {
    'id_mission': lambda valeur: len(valeur) > 0,
    'Nom': lambda valeur:  valeur == '' or bool(re.match('^[a-zA-Z0-9 ]+$', valeur)),
    'Prenom': lambda valeur:  valeur == '' or bool(re.match('^[a-zA-Z0-9 ]+$', valeur)),
    'telephone': lambda valeur: valeur == '' or bool(re.match('^(?:\+|0)[1-9](?:[ .-]?[0-9]{2}){4}$', valeur)),
    'Ville': lambda valeur:valeur == '' or bool(re.match('^[a-zA-Z0-9 ]+$', valeur)),
    'Payer': lambda valeur: valeur == '' or bool(re.match('^[a-zA-Z0-9 ]+$', valeur)),
    'Adresse': lambda valeur: valeur == '' or bool(re.match('^[a-zA-Z0-9\s\-\,\']+', valeur))
    }


    id_mission = request.form.get('id_mission')
    Nom = request.form.get('Nom')
    Prenom = request.form.get('Prenom')
    date = request.form.get('date')
    Sexe = request.form.get('Sexe')
    Age = request.form.get('Age')
    CIN = request.form.get('CIN')
    telephone = request.form.get('telephone')
    Ville = request.form.get('Ville')
    Payer = request.form.get('Payer')
    Adresse = request.form.get('Adresse')
    
    image_file = request.files['profil']
    image_data = image_file.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    messages_erreur = {}
    for nom_champ, contrainte in contraintes.items():
        valeur_champ = request.form.get(nom_champ)
        if not contrainte(valeur_champ):
           messages_erreur[nom_champ] = f"champ invalide"
    
   # Insérer les information patient dans la base de données
    nombre_elements1 = db.Info_patient.count_documents({})
    idPatient = "P" + str(nombre_elements1)
    idutilisateur = session['utilisateur_id']
    
    
 
   ###################################################################################################
        
    Numero_dossier_medical = request.form.get('Numero_dossier_medical')
    Mode_Transport = request.form.get('Mode_Transport')
    Date_Transport = request.form.get('Date_Transport')
    Nom_Medcin_Traitant = request.form.get('Nom_Medcin_Traitant')
    Service_Medical = request.form.get('Service_Medical')
    Hopitale_Destination = request.form.get('Hopitale_Destination')
    Heur_Transport = request.form.get('Heur_Transport')
    infirmier = request.form.get('infirmier')
    
    
   # Insérer les information patient dans la base de données
    nombre_elements1 = db.transfererPatient.count_documents({})
    idtrans = "tr" + str(nombre_elements1)

    if not messages_erreur: 
        info_patient = {"_id":idPatient,
                        "id_mission":id_mission,
                        "Nom": Nom,
                        "Prenom": Prenom,
                        "date_naissance": date,
                        "Sexe": Sexe,
                        "Age": Age,
                        'image': image_base64,
                        "CIN": CIN,
                        "telephone": telephone,
                        "Ville": Ville,
                        "Payer": Payer,
                        "Adresse": Adresse,
                        "idutilisateur": idutilisateur}

        db.Info_patient.insert_one(info_patient)
        
        nombre_elements1 = db.transfererPatient.count_documents({})
        idtrans = "tr" + str(nombre_elements1)
        info_trans = {"_id": idtrans,
              "idPatient": idPatient,
              "id_mission": id_mission,
              "Numero_dossier_medical": Numero_dossier_medical,
              "Mode_Transport": Mode_Transport,
              "Date_Transport": Date_Transport,
              "Nom_Medcin_Traitant": Nom_Medcin_Traitant,
              "Service_Medical": Service_Medical,
              "Hopitale_Destination": Hopitale_Destination,
              "Heur_Transport": Heur_Transport,
              "infirmier": infirmier,
              "idutilisateur": idutilisateur}

        nombre_champs_remplis = len([value for value in info_trans.values() if value != ""])
        if nombre_champs_remplis > 4:
            db.transfererPatient.insert_one(info_trans)
  ###########################################################################################################   
    
        historique_Médical2 = request.form.getlist('Historique_Médical2')
        historique_autres = request.form.get('Historique_Médical2')

        if historique_autres and historique_autres not in historique_Médical2:
            historique_Médical2.append(historique_autres)

        info_historique={"idPatient": idPatient,
                        "id_mission":id_mission,
                        "historique":historique_Médical2
                        }
        db.historique.insert_one(info_historique)
    
    ###########################################################################################################   
    
        Allergies_liste = request.form.getlist('Allergies1')
        Allergies_autres = request.form.get('Allergies1')

        if Allergies_autres  and Allergies_autres!="" and Allergies_autres not in Allergies_liste:
            Allergies_liste.append(Allergies_autres)

        info_Allergies={"idPatient": idPatient,
                     "id_mission":id_mission,
                     "Allergies":Allergies_liste
                     }   
        db.Allergies.insert_one(info_Allergies)
  ##########################################################################################################
  
        autre_soin = request.form.get('autre_soin')
        
        text_autre_soin={"idPatient": idPatient,
                        "id_mission":id_mission,
                        "autre_soin":autre_soin
                        }
        db.autre_soin.insert_one(text_autre_soin)
  ##########################################################################################################
  
  
    
    donnees_liste = request.form.getlist('table1donnees')
    nb_champs = 5
    nb_lignes = len(donnees_liste) // nb_champs
    lignes = []
    for i in range(nb_lignes):
        ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
        lignes.append(ligne)

    
    if not messages_erreur:
        for ligne in lignes:
            
            nombre_elements3 = db.soin.count_documents({})
            idsoin = "S" + str(nombre_elements3)
            db.soin.insert_one({"_id":idsoin,
                                'Niveau_de_conscience':ligne[0],
                                'Fréquence_cardiaque': ligne[1],
                                'Pression_artérielle': ligne[2],
                                'Température': ligne[3],
                                'Respiration':ligne[4],
                                "idPatient": idPatient,
                                'id_mission': id_mission,
                                "idutilisateur": idutilisateur})
  
            
    # ----------------------------------------------------------------------------
    donnees_liste = request.form.getlist('table2donnees')
    nb_champs = 3
    nb_lignes = len(donnees_liste) // nb_champs
    lignes = []
    for i in range(nb_lignes):
        ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
        lignes.append(ligne)

    if not messages_erreur:
        for ligne in lignes:
            nombre_elements3 = db.blessures.count_documents({})
            idblessure = "BL" + str(nombre_elements3)
            db.blessures.insert_one({"_id":idblessure,
                                    'Type_de_blessures': ligne[0],
                                    'Emplacement_des_blessures': ligne[1],
                                    'Gravité_des_blessures': ligne[2],
                                    "idPatient": idPatient,
                                    'id_mission': id_mission,
                                    "idutilisateur": idutilisateur})
            
        return render_template("modal_imprimer.html" , info_patient=info_patient , page = "patient"  )
    
    if verifierSession() == "Personnel médical Membre" :
        return render_template("personnel_medical.html" , poste ="Personnel médical Membre" ,messages_erreur=messages_erreur ,missions=mission )
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("personnel_medical.html" , poste ="Responsable de sécurité Membre" ,messages_erreur=messages_erreur ,missions=mission  )
    
