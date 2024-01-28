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

@app.route("/chercher_deces")
def chercher_deces():
    messages_erreur = {}
    
    idU = session['utilisateur_id']
    mission = db.affectation.find({ 'idmembre': idU})
    
    index_deces = request.args.get('id_decedes')
    patient = db.Info_decedes.count_documents({"_id": index_deces})
    
    if patient != 0:
        return redirect(url_for('Modifier_info_deces', id_decedes=index_deces))
    else:
        if verifierSession() == "Personnel médical Membre" :
            return render_template("personnes_decedes.html" , poste ="Personnel médical Membre" ,messages_erreur=messages_erreur ,missions=mission  )
        if verifierSession() == "Responsable de sécurité Membre" :
            return render_template("personnes_decedes.html" , poste ="Responsable de sécurité Membre" ,messages_erreur=messages_erreur ,missions=mission )


@app.route('/Modifier_info_deces/<id_decedes>')
def Modifier_info_deces(id_decedes): 
    
    idU = session['utilisateur_id']
    mission = db.affectation.find({ 'idmembre': idU})
    
    messages_erreur = request.args.get('messages_erreur', '')
        
    index_deces = db.Info_decedes.find_one({"_id": id_decedes})
    
    if verifierSession() == "Personnel médical Membre" :
        return render_template("modifier_decedes.html", poste="Personnel médical Membre", messages_erreur=messages_erreur, info_patient=index_deces ,missions=mission)
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("modifier_decedes.html", poste="Responsable de sécurité Membre", messages_erreur=messages_erreur, info_patient=index_deces ,missions=mission)
     
@app.route("/modifier_deces" , methods=['POST'])
def modifier_deces():
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
    
    idDeces = request.form.get('Index')
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
    
   
    idutilisateur = session['utilisateur_id']
    
    
    if not messages_erreur:
        filter = {'_id': idDeces}
        update = { '$set':{"_id": idDeces,
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
                        "date_deces":date_deces,
                        "heure_deces":heure_deces,
                        "Lieu_deces":Lieu_deces,
                        "Caus_deces":Caus_deces,
                        "Cause_medicale_deces": Cause_medicale_deces,
                        "idutilisateur": idutilisateur}}
    
     
        db.Info_decedes.update_one(filter, update) 
        
    info_patient = db.Info_decedes.find_one({"_id": idDeces})        
    
    if verifierSession() == "Personnel médical Membre" :
        return render_template("modifier_decedes.html", poste="Personnel médical Membre", messages_erreur=messages_erreur, info_patient=info_patient ,missions=mission)
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("modifier_decedes.html", poste="Responsable de sécurité Membre", messages_erreur=messages_erreur, info_patient=info_patient ,missions=mission)
        