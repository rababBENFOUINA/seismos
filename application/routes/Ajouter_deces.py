import base64
import re
from bson.binary import Binary
from application import app
from flask import Flask, Blueprint, render_template, request, session
from pymongo import MongoClient
from application import db
from application.routes.acceuil import verifierSession

@app.route("/formulaire_ajouter_decedes")
def afficher_ajouter_decedes():
    messages_erreur = {}
    info_decedes={}
    
    idU = session['utilisateur_id']
    mission = db.affectation.find({ 'idmembre': idU})
    
    if verifierSession() == "Personnel médical Membre" :
        return render_template("personnes_decedes.html" , poste ="Personnel médical Membre" ,messages_erreur=messages_erreur ,missions=mission , info_decedes=info_decedes )
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("personnes_decedes.html" , poste ="Responsable de sécurité Membre" ,messages_erreur=messages_erreur ,missions=mission , info_decedes=info_decedes )
 
@app.route("/ajouter_decedes" , methods=['POST'])
def ajouter_decedes():
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
    date_deces = request.form.get('date_deces')
    heure_deces = request.form.get('heure_deces')
    Lieu_deces = request.form.get('Lieu_deces')
    Caus_deces = request.form.get('Caus_deces')
    Cause_medicale_deces = request.form.get('Caus_deces')
    
    image_file = request.files['profil']
    image_data = image_file.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    messages_erreur = {}
    for nom_champ, contrainte in contraintes.items():
        valeur_champ = request.form.get(nom_champ)
        if not contrainte(valeur_champ):
           messages_erreur[nom_champ] = f"champ invalide"
    
   # Insérer les information patient dans la base de données
    nombre_elements1 = db.Info_decedes.count_documents({})
    idDecedes = "D" + str(nombre_elements1)
    idutilisateur = session['utilisateur_id']
    
    if not messages_erreur: 
        info_Decedes = {"_id":idDecedes,
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
                        "date_deces": date_deces,
                        "heure_deces": heure_deces,
                        "Lieu_deces": Lieu_deces,
                        "Caus_deces": Caus_deces,
                        "Cause_medicale_deces": Cause_medicale_deces,
                        "idutilisateur": idutilisateur}

        db.Info_decedes.insert_one(info_Decedes)
        
        return render_template("modal_imprimer.html" , info_patient=info_Decedes , page = "decedes" )
    
    if verifierSession() == "Personnel médical Membre" :
        return render_template("personnes_decedes.html" , poste ="Personnel médical Membre" ,messages_erreur=messages_erreur ,missions=mission )
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("personnes_decedes.html" , poste ="Responsable de sécurité Membre" ,messages_erreur=messages_erreur ,missions=mission  )
    
    
