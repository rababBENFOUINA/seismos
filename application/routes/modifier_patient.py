import base64
import datetime
import json
import re
from bson.binary import Binary
import folium
from application import app
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from application import db
from application.routes.acceuil import verifierSession

@app.route("/chercher_patient")
def chercher_patient():
    messages_erreur = {}
    
    idU = session['utilisateur_id']
    mission = db.affectation.find({ 'idmembre': idU})
    
    index_patient = request.args.get('indexPatient')
    patient = db.Info_patient.count_documents({"_id": index_patient})
    
    if patient != 0:
        return redirect(url_for('Modifier_info_patient', id_patient=index_patient))
    else:
        if verifierSession() == "Personnel médical Membre" :
            return render_template("personnel_medical.html" , poste ="Personnel médical Membre" ,messages_erreur=messages_erreur ,missions=mission  )
        if verifierSession() == "Responsable de sécurité Membre" :
            return render_template("personnel_medical.html" , poste ="Responsable de sécurité Membre" ,messages_erreur=messages_erreur ,missions=mission )
        

@app.route('/Modifier_info_patient/<id_patient>')
def Modifier_info_patient(id_patient): 
    
    idU = session['utilisateur_id']
    mission = db.affectation.find({ 'idmembre': idU})
    
    messages_erreur = request.args.get('messages_erreur', '')
        
    info_patient = db.Info_patient.find_one({"_id": id_patient})
    info_trans = db.transfererPatient.find({"idPatient": id_patient})
    historique = db.historique.find({"idPatient": id_patient})
    Allergies = db.Allergies.find({"idPatient": id_patient})
    soin = db.soin.find({"idPatient": id_patient})
    blessures=db.blessures.find({"idPatient": id_patient})
    autre_soin=db.autre_soin.find_one({"idPatient": id_patient})
    
    if verifierSession() == "Personnel médical Membre" :
        return render_template("modifier_info_patient.html", poste="Personnel médical Membre", messages_erreur=messages_erreur, info_patient=info_patient ,info_trans=info_trans ,historique=historique,Allergies=Allergies,soin=soin,blessures=blessures,autre_soin=autre_soin,missions=mission)
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("modifier_info_patient.html", poste="Responsable de sécurité Membre", messages_erreur=messages_erreur, info_patient=info_patient ,info_trans=info_trans ,historique=historique,Allergies=Allergies,soin=soin,blessures=blessures,autre_soin=autre_soin,missions=mission)
    
    
   
@app.route("/modifier_patient" , methods=['POST'])
def modifier_patient():

    idU = session['utilisateur_id'] 
    mission = db.affectation.find({ 'idmembre': idU})
    
    contraintes = {
    'id_mission': lambda valeur: len(valeur) > 0,
    'Nom': lambda valeur:  valeur == '' or bool(re.match('^[a-zA-Z0-9 ]+$', valeur)),
    'Prenom': lambda valeur:  valeur == '' or bool(re.match('^[a-zA-Z0-9 ]+$', valeur)),
    'telephone': lambda valeur:  valeur == '' or bool(re.match('^+0[1-9][0-9]{20}$', valeur)),
    'Ville': lambda valeur:valeur == '' or bool(re.match('^[a-zA-Z0-9 ]+$', valeur)),
    'Payer': lambda valeur: valeur == '' or bool(re.match('^[a-zA-Z0-9 ]+$', valeur)),
    'Adresse': lambda valeur: valeur == '' or bool(re.match('^[a-zA-Z0-9\s\-\,\']+', valeur))
    }

    idPatient = request.form.get('idPatient')
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
    
    if not messages_erreur:
        filter = {'_id': idPatient}
        update = { '$set':{"_id": idPatient,
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
                        "idutilisateur": idutilisateur}}
    
     
        db.Info_patient.update_one(filter, update)
     
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
        
        resultat = db.historique.find_one({"$and":[{"idPatient": idPatient},{"id_mission": id_mission}]})
        if resultat:
            update3={ '$set':{ "idPatient": idPatient,
                    "id_mission":id_mission,
                    "historique":historique_Médical2
                    }}
            db.historique.update_one(resultat, update3)
        else:    
            db.historique.insert_one(info_historique)
        
    ################################################################################################
    
        Allergies_liste = request.form.getlist('Allergies1')
        Allergies_autres = request.form.get('Allergies1')

        if Allergies_autres  and Allergies_autres!="" and Allergies_autres not in Allergies_liste:
            Allergies_liste.append(Allergies_autres)

        info_Allergies={"idPatient": idPatient,
                     "id_mission":id_mission,
                     "Allergies":Allergies_liste
                     }
        
        resultat2 = db.Allergies.find_one({"$and":[{"idPatient": idPatient},{"id_mission": id_mission}]})
        if resultat2:
            update4={ '$set':{"idPatient": idPatient,
                     "id_mission":id_mission,
                     "Allergies":Allergies_liste
                     }}
            db.Allergies.update_one(resultat2, update4)
        else:    
            db.Allergies.insert_one(info_Allergies)
            
    ############################################################################################################################
        autre_soin1 = request.form.get('autre_soin')
        autre_soin_dict={"idPatient": idPatient,
                        "id_mission": id_mission,
                        "autre_soin": autre_soin1
                        }
        
        resultat3 = db.autre_soin.find_one({"$and":[{"idPatient": idPatient},{"id_mission": id_mission}]})
        if resultat3:
            update5={'$set': {"idPatient": idPatient,
                        "id_mission": id_mission,
                        "autre_soin": autre_soin1
                        }}
            db.autre_soin.update_one(resultat3, update5)
        else:    
            db.autre_soin.insert_one(autre_soin_dict)

    ################################################################################################
    donnees_liste = request.form.getlist('table1donnees')
    nb_champs = 6
    nb_lignes = len(donnees_liste) // nb_champs
    lignes = []
    for i in range(nb_lignes):
        ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
        lignes.append(ligne)

    if not messages_erreur:
        for ligne in lignes:
            id = ligne[1]
            resultat3 = db.soin.find_one({"_id":id})
            if resultat3:
                update5 = {'$set': {
                                    'Niveau_de_conscience':ligne[0],
                                    'Fréquence_cardiaque': ligne[2],
                                    'Pression_artérielle': ligne[3],
                                    'Température': ligne[4],
                                    'Respiration':ligne[5],
                                    "idPatient": idPatient,
                                    'id_mission': id_mission,
                                    "idutilisateur": idutilisateur}}

                db.soin.update_one(resultat3, update5)

            else:
                nombre_elements3 = db.soin.count_documents({})
                idsoin = "S" + str(nombre_elements3)
                db.soin.insert_one({"_id":idsoin,
                                    'Niveau_de_conscience':ligne[0],
                                    'Fréquence_cardiaque': ligne[2],
                                    'Pression_artérielle': ligne[3],
                                    'Température': ligne[4],
                                    'Respiration':ligne[5],
                                    "idPatient": idPatient,
                                    'id_mission': id_mission,
                                    "idutilisateur": idutilisateur})
                
    #################################################################################################################
    donnees_liste = request.form.getlist('table2donnees')
    nb_champs = 4
    nb_lignes = len(donnees_liste) // nb_champs
    lignes = []
    for i in range(nb_lignes):
        ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
        lignes.append(ligne)

    if not messages_erreur:
        for ligne in lignes:
            id = ligne[0]
            resultat3 = db.blessures.find_one({"_id":id})
            if resultat3:
                update5 = {'$set': {
                                    'Type_de_blessures': ligne[1],
                                    'Emplacement_des_blessures': ligne[2],
                                    'Gravité_des_blessures': ligne[3],
                                    "idPatient": idPatient,
                                    'id_mission': id_mission,
                                    "idutilisateur": idutilisateur}}

                db.blessures.update_one(resultat3, update5)

            else:
                nombre_elements3 = db.blessures.count_documents({})
                idblessure = "BL" + str(nombre_elements3)
                db.blessures.insert_one({"_id":idblessure,
                                        'Type_de_blessures': ligne[1],
                                        'Emplacement_des_blessures': ligne[2],
                                        'Gravité_des_blessures': ligne[3],
                                        "idPatient": idPatient,
                                        'id_mission': id_mission,
                                        "idutilisateur": idutilisateur})
            
        
    info_patient = db.Info_patient.find_one({"_id": idPatient})
    info_trans = db.transfererPatient.find({"idPatient": idPatient})
    historique = db.historique.find({"idPatient": idPatient})
    Allergies = db.Allergies.find({"idPatient": idPatient})
    soin = db.soin.find({"idPatient": idPatient})
    blessures=db.blessures.find({"idPatient": idPatient})
    autre_soin=db.autre_soin.find_one({"idPatient": idPatient})
    
    if verifierSession() == "Personnel médical Membre" :
        return render_template("modifier_info_patient.html", poste="Personnel médical Membre", messages_erreur=messages_erreur, info_patient=info_patient ,info_trans=info_trans ,historique=historique,Allergies=Allergies,soin=soin,blessures=blessures,autre_soin=autre_soin,missions=mission)
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("modifier_info_patient.html", poste="Responsable de sécurité Membre", messages_erreur=messages_erreur, info_patient=info_patient ,info_trans=info_trans ,historique=historique,Allergies=Allergies,soin=soin,blessures=blessures,autre_soin=autre_soin,missions=mission)
    

    
                
    
    #messages_erreur_str = "&".join([f"{key}={val}" for key, val in messages_erreur.items()])
    #return redirect(url_for('Modifier_info_patient', id_patient=idPatient, messages_erreur=messages_erreur_str,missions=mission))
    

@app.route("/imprimer/<id>")
def imprimer(id):
    info_patient = db.Info_patient.find_one({"_id":id})
    
    return render_template("modal_imprimer.html" , info_patient=info_patient )
    
    