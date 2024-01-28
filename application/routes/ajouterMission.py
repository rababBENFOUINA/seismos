
import datetime
import re
import folium
from application import app
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from application import db
from application.routes.acceuil import verifierSession


@app.route("/ajouter_mission_exploration")
def affiche_formulaire_ajouter_tache():
    messages_erreur = {}
    
    chef = db.utilisateur.find({
        "$or": [
            {"role": "Chef d'équipe"},
            {"poste": "Responsable de matériel"},
            {"poste": "Responsable d'etat"}
        ],
        "$and": [
            {"poste": {"$ne": "Personnel médical"}},
            {"poste": {"$ne": "Responsable de sécurité"}},
            {"poste": {"$ne": "Coordonnateur"}}
        ]
    })
    

  # Créer une carte centrée sur un emplacement spécifique
    mapObj = folium.Map(location=[32.319235, -6.350351], zoom_start=1.5)

    # Ajouter la couche de tuiles Esri WorldStreetMap
    tile_layer = folium.raster_layers.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri WorldStreetMap',
        overlay=False,
        control=True
    ).add_to(mapObj)

    # Rendre la carte dans un template HTML
    map_html = mapObj._repr_html_()
    
    if verifierSession() == "Coordonnateur" :
        return render_template("CreeMissionExploration.html" , poste ="Coordonnateur" ,messages_erreur=messages_erreur,chef=chef, map_html=map_html, Type_mission=session['type_mission'])
   
   
   
   
#########################################################################################################
@app.route('/ajouter_mission_exploration', methods=['POST'])
def ajouter_Mission_exploration():
    if request.method == 'POST':
        chef = db.utilisateur.find({
                "$or": [
                    {"role": "Chef d'équipe"},
                    {"poste": "Responsable de matériel"},
                    {"poste": "Responsable d'etat"}
                ],
                "$and": [
                    {"poste": {"$ne": "Personnel médical"}},
                    {"poste": {"$ne": "Responsable de sécurité"}},
                    {"poste": {"$ne": "Coordonnateur"}}
                ]
            })
        # Définition des contraintes pour chaque champ
        contraintes = {
            'Nom': lambda valeur: len(valeur) > 0 and len(valeur) <= 50 and bool(re.match('^[a-zA-Z-0-9 ]+$', valeur)),
            'Objectif': lambda valeur: len(valeur) > 0 and len(valeur) <= 500 and bool(re.match('^[a-zA-Z-0-9 ]+$', valeur)),
            'Date_deb': lambda valeur: len(valeur) > 0 and datetime.datetime.strptime(valeur, '%Y-%m-%d') >= datetime.datetime.now(),
            'Date_fin': lambda valeur: verifier_date_fin(valeur, date_deb) if len(valeur) > 0 else True

        }
        
        nom = request.form.get('Nom')
        objectif = request.form.get('Objectif')
        date_deb = request.form.get('Date_deb')
        date_fin = request.form.get('Date_fin')

    messages_erreur = {}
    for nom_champ, contrainte in contraintes.items():
        valeur_champ = request.form.get(nom_champ)
        if not contrainte(valeur_champ):
            messages_erreur[nom_champ] = f"Ce champ est invalide"

    # Insérer la mission dans la base de données
    nombre_elements1 = db.mission.count_documents({})
    idMission = "M" + str(nombre_elements1)
    idcoordonnateur = session['utilisateur_id']

    if not messages_erreur:
        info_mission = {"_id": idMission,
                        "Nom": nom,
                        "Objectif": objectif,
                        "Date_deb": date_deb,
                        "Date_fin": date_fin,
                        "Type": "exploration",
                        "idcoordonnateur": idcoordonnateur}

        db.mission.insert_one(info_mission)

    # ----------------------------------------------------------------------------
    donnees_liste = request.form.getlist('table1donnees')
    nb_champs = 3
    nb_lignes = len(donnees_liste) // nb_champs
    lignes = []
    for i in range(nb_lignes):
        ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
        lignes.append(ligne)

    if not messages_erreur:
        for ligne in lignes:

            nombre_elements2 = db.finance.count_documents({})
            idFinance = "F" + str(nombre_elements2)
            db.finance.insert_one({"_id": idFinance,
                                   'Financier': ligne[0],
                                   'budget': ligne[1],
                                   'date_de_financement': ligne[2],
                                   'id_mission': idMission,
                                   "idcoordonnateur": idcoordonnateur})

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
                nombre_elements2 = db.equipement.count_documents({})
                idEquipement = "EQP" + str(nombre_elements2)
                db.equipement.insert_one({
                    '_id':idEquipement,
                'Nom_equipement': ligne[0],
                'quantite': ligne[1],
                'equipe': ligne[2],
                'id_mission': idMission,
                "idcoordonnateur": idcoordonnateur})

    # ----------------------------------------------------------------------------
    donnees_liste = request.form.getlist('table3donnees')
    nb_champs = 5
    nb_lignes = len(donnees_liste) // nb_champs
    lignes = []
    for i in range(nb_lignes):
        ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
        lignes.append(ligne)
        
   
    if not messages_erreur:
        mail_destinataire=""
        for ligne in lignes:
            nombre_elements3 = db.calendrierMission.count_documents({})
            idEqMission = "EQ" + str(nombre_elements3)
            
            
            chef_equipe=ligne[0]
            chef=db.utilisateur.find_one({"_id":chef_equipe})
            if chef and 'email' in chef and chef['email']:
                if chef['poste']=="Responsable d'etat":
                    mail_destinataire=chef['email']
                  
                
            db.calendrierMission.insert_one({"_id": idEqMission,
                                             'chef_equipe': ligne[0],
                                             'Nom_equipe': ligne[1],
                                             'tache': ligne[2],
                                             'date_debut': ligne[3],
                                             'date_fin': ligne[4],
                                             'id_mission': idMission,
                                             "idcoordonnateur": idcoordonnateur})
    # ----------------------------------------------------------------------------------

    # Créer une carte centrée sur un emplacement spécifique
    mapObj = folium.Map(location=[32.319235, -6.350351], zoom_start=1.5)

    # Ajouter la couche de tuiles Esri WorldStreetMap
    tile_layer = folium.raster_layers.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri WorldStreetMap',
        overlay=False,
        control=True
    ).add_to(mapObj)

    # Rendre la carte dans un template HTML
    map_html = mapObj._repr_html_()

    if 'lat' in session.keys() and 'lon' in session.keys() and 'rayon' in session.keys():
        lat = session['lat']
        lon = session['lon']
        rayon = session['rayon']
        
        if not messages_erreur:
            nombre_elements2 = db.equipement.count_documents({})
            idLocalisation = "Loc" + str(nombre_elements2)
            data = {
                "_id":idLocalisation,
                'lat': lat,
                'lon': lon,
                'rayon': rayon,
                'id_mission': idMission,
                'idcoordonnateur': idcoordonnateur}
            db.locatisation.insert_one(data)
        
        session.pop('lat',None)
        session.pop('lon',None)
        session.pop('rayon',None)


    if verifierSession() == "Coordonnateur" and messages_erreur :
        return render_template("CreeMissionExploration.html" , poste ="Coordonnateur" ,messages_erreur=messages_erreur,chef=chef, map_html=map_html , Type_mission=session['type_mission'])
    elif mail_destinataire != "" :
        return render_template("mail_to_resp.html",mission= idMission , nom=nom, obj= objectif ,Date_deb=date_deb ,mail_destinataire=mail_destinataire)
    else:
        return redirect(url_for("affiche_formulaire_ajouter_tache"))


def verifier_date_fin(date_fin, date_deb):
    if date_fin < date_deb:
        return False
    else:
        return True
