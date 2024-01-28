import datetime
import re
from application import app
from flask import Flask,Blueprint, render_template, request, session 
from pymongo import MongoClient
from application import db
import os
import base64

from application.routes.acceuil import verifierSession

@app.route("/AjoutRapport")
def Ajout_rapport():
    messages_erreur = {}
    
    idmembre=session['utilisateur_id']
    if verifierSession() == "Coordonnateur" :
            missions1 = db.mission.find({'idcoordonnateur': idmembre})
            mission1 = list(missions1)
            missions = []
            for mission in mission1:
                missions.append(mission['_id'])

    else:
            missions2=db.calendrierMission.find({'chef_equipe':idmembre})
            
            missions = []
            for mission in missions2:
                missions.append(mission['id_mission'])
            
            
    if verifierSession() == "Coordonnateur" :
        return render_template("Ajouter_rapport.html" , poste ="Coordonnateur" , messages_erreur=messages_erreur , missions=missions , Type_mission=session['type_mission'])
    if verifierSession() == "Responsable de matériel" :
        return render_template("Ajouter_rapport.html" , poste ="Responsable de matériel" , messages_erreur=messages_erreur , missions=missions,Type_mission=session['type_mission'])
    if verifierSession() == "Responsable d'etat" :
            return render_template("Ajouter_rapport.html" , poste ="Responsable d'etat" , messages_erreur=messages_erreur , missions=missions,Type_mission=session['type_mission'])
    if verifierSession() == "Personnel médical Chef" :
            return render_template("Ajouter_rapport.html" , role = "Personnel médical Chef" , messages_erreur=messages_erreur , missions=missions,Type_mission=session['type_mission'])
    if verifierSession() == "chef" :
            return render_template("Ajouter_rapport.html" , role = "chef" , messages_erreur=messages_erreur , missions=missions,Type_mission=session['type_mission'])
    if verifierSession() == "Sismologue" :
            return render_template("Ajouter_rapport.html" , poste = "Sismologue" , messages_erreur=messages_erreur , missions=missions,Type_mission=session['type_mission'])


@app.route('/AjoutRapport', methods=['POST'])
def ajoutrapport():
    if request.method == 'POST':
        idmembre=session['utilisateur_id']
        info_user = db.utilisateur.find_one({'_id': idmembre})
        
        if verifierSession() == "Coordonnateur" :
            mission1=db.mission.find({'idcoordonnateur':idmembre})
            missions = []
            for mission in mission1:
                missions.append(mission['_id'])
        else:
            mission2=db.calendrierMission.find({'chef_equipe':idmembre})
            missions = []
            for mission in mission2:
                missions.append(mission['id_mission'])
        
        
         
            
        # Définition des contraintes pour chaque champ
        contraintes = {
            'titre_rapport': lambda valeur: len(valeur) > 0 and len(valeur) <= 50 and bool(re.match('^[a-zA-Z-0-9 ]+$', valeur)),
            'id_mission' :lambda valeur : mission_existe_pas(valeur),
            
        }
        id = request.form.get('id')
        titre_rapport = request.form.get('titre_rapport')
        id_mission = request.form.get('id_mission')
        Description = request.form.get('description')
        type =request.form.get('Type')
        
        if verifierSession() == "Coordonnateur":
            Destinataire = request.form.get('Destinataire')
        else :
              Destinataire  = "Coordonnateur"
              
        nombre_elements = db.rapport.count_documents({})
        idEquipement = "RP" + str(nombre_elements)    
        pdf_file = request.files['rapport_pdf']
        data = pdf_file.read()
        encoded_data = base64.b64encode(data).decode('utf-8')
        
        messages_erreur = {}
        for nom_champ, contrainte in contraintes.items():
            valeur_champ = request.form.get(nom_champ)
            if not contrainte(valeur_champ):
                messages_erreur[nom_champ] = f"Ce champ est invalide"
                
        date_systeme = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        date_str = date_systeme.strftime('%Y-%m-%d')
        if not messages_erreur: 
            rapport = {"_id": idEquipement,
                                "idemetteur":id,
                                "titre_rapport": titre_rapport,
                                "id_mission": id_mission,
                                "Destinataire": Destinataire,
                                "Date_depot": date_str,
                                'name': pdf_file.filename,
                                'data': encoded_data,
                                'Description':Description,
                                'expediteu':info_user['poste'],
                                'type':type
                                }   
            db.rapport.insert_one(rapport)
            
            
            
        if verifierSession() == "Coordonnateur" :
            return render_template("Ajouter_rapport.html" , poste ="Coordonnateur" , messages_erreur=messages_erreur , missions=missions , Type_mission=session['type_mission'])
        if verifierSession() == "Responsable de matériel" :
            return render_template("Ajouter_rapport.html" , poste ="Responsable de matériel" , messages_erreur=messages_erreur , missions=missions)
        if verifierSession() == "Responsable d'etat" :
            return render_template("Ajouter_rapport.html" , poste ="Responsable d'etat" , messages_erreur=messages_erreur , missions=missions)
        if verifierSession() == "Personnel médical Chef" :
            return render_template("Ajouter_rapport.html" , role ="Personnel médical Chef" , messages_erreur=messages_erreur , missions=missions)
        if verifierSession() == "chef" :
            return render_template("Ajouter_rapport.html" , role ="chef" , messages_erreur=messages_erreur , missions=missions)



def mission_existe_pas(id):
    missions = db.mission.distinct("_id")
    for i in missions :
        if id==i :
            return True
    return False