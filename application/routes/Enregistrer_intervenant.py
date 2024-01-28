import base64
import re
from bson.binary import Binary
from application import app
from flask import Flask, Blueprint, render_template, request, session
from pymongo import MongoClient
from application import db
from application.routes.acceuil import verifierSession

@app.route("/Page_ajouter_intervenant")
def page_ajouter_intervenant():
    messages_erreur = {}
    
    idU = session['utilisateur_id']
    mission = db.affectation.find({ 'idmembre': idU})
    
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("Enregistrer_intervenant.html" , poste ="Responsable de sécurité Membre" ,messages_erreur=messages_erreur ,missions=mission )


@app.route("/ajouter_intervenant" , methods=['POST'])
def ajouter_intervenant():
    if request.method == 'POST':
        idU = session['utilisateur_id'] 
        mission = db.affectation.find({ 'idmembre': idU})

        contraintes = {
        'id_mission': lambda valeur: len(valeur) > 0,
        'Nom': lambda valeur: bool(re.match('^[a-zA-Z0-9 ]+$', valeur)),
        'Prenom': lambda valeur: bool(re.match('^[a-zA-Z0-9 ]+$', valeur)),
        'Sexe': lambda valeur: len(valeur) > 0,
        'telephone': lambda valeur: valeur == '' or bool(re.match('^(?:\+|0)[1-9](?:[ .-]?[0-9]{2}){4}$', valeur)),
        'nationalite': lambda valeur: len(valeur) > 0,
        'CIN': lambda valeur: bool(re.match('^[a-zA-Z0-9\s\-\,\']+', valeur)),
        'role': lambda valeur: valeur in ['journaliste', 'volontaire']
        }

        id_mission = request.form.get('id_mission')
        Nom = request.form.get('Nom')
        Prenom = request.form.get('Prenom')
        Sexe = request.form.get('Sexe')
        Age = request.form.get('Age')
        CIN = request.form.get('CIN')
        telephone = request.form.get('telephone')
        Adresse = request.form.get('Adresse')
        role = request.form.get('role')
        nationalite = request.form.get('nationalite')
        badge = request.form.get('badge')
        media = request.form.get('media')
        coverage = request.form.get('coverage')
        equipment = request.form.get('equipment')
        organization = request.form.get('organization')
        activity = request.form.get('activity')
        contactOrg = request.form.get('contactOrg')
        adresseOrg = request.form.get('adresseOrg')
        
        image_file = request.files['profil']
        image_data = image_file.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        messages_erreur = {}
        for nom_champ, contrainte in contraintes.items():
            valeur_champ = request.form.get(nom_champ)
            if not contrainte(valeur_champ):
                messages_erreur[nom_champ] = f"champ invalide"

        
        
        nombre_elements1 = db.Intervenant.count_documents({})
        idIntervenant = "I" + str(nombre_elements1)
        idutilisateur = session['utilisateur_id']

        if not messages_erreur and role == "journaliste": 
            db.Intervenant.insert_one({"_id":idIntervenant,
                            "Role":role,
                            "id_mission":id_mission,
                            "Nom": Nom,
                            "Prenom": Prenom,
                            "Sexe": Sexe,
                            "Age": Age,
                            'image': image_base64,
                            "CIN": CIN,
                            "telephone": telephone,
                            "Nationalite":nationalite,
                            "Adresse": Adresse,
                            "idutilisateur": idutilisateur,
                            "badge":badge,
                            "Media":media,
                            "DomaineDeCouverture":coverage,
                            "Equipement":equipment})
        elif not messages_erreur and role == "volontaire":
            db.Intervenant.insert_one({"_id":idIntervenant,
                            "Role":role,
                            "id_mission":id_mission,
                            "Nom": Nom,
                            "Prenom": Prenom,
                            "Sexe": Sexe,
                            "Age": Age,
                            'image': image_base64,
                            "CIN": CIN,
                            "telephone": telephone,
                            "Nationalite":nationalite,
                            "Adresse": Adresse,
                            "idutilisateur": idutilisateur,
                            "Organisation":organization,
                            "ActiviteOrg":activity,
                            "ContactOrg":contactOrg,
                            "AdresseOrg":adresseOrg})
        

        return render_template("Enregistrer_intervenant.html" , poste ="Responsable de sécurité Membre" ,messages_erreur=messages_erreur ,missions=mission )
