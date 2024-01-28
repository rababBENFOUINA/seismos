import datetime
import re
from tarfile import RECORDSIZE
from application import app
from flask import flash, redirect, render_template,request, session, url_for
from application import db
import folium

from application.routes.acceuil import verifierSession

@app.route('/modifier_mission_exploration/<id>')
def modifier_mission_exploration(id):
    #chef = db.utilisateur.find({"$or": [{"role": "Chef d'équipe"}, {"poste": "Responsable de matériel"}, {"poste": "Responsable d'etat"}]})
    mission = db.mission.find_one({'_id':id})
    
    if mission['Type'] == "exploration" :
        
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
    
        
        donnees= db.locatisation.find({ 'id_mission': id })
        
        documents = list(donnees)
        if documents:
            document = documents[0]
            lat = document['lat']
            lon = document['lon']
            rayon = document['rayon']

            mapObj = folium.Map(location=[lat,lon], zoom_start=5)

            # Ajouter la couche de tuiles Esri WorldStreetMap
            tile_layer = folium.raster_layers.TileLayer(
                tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
                attr='Esri',
                name='Esri WorldStreetMap',
                overlay=False,
                control=True
            ).add_to(mapObj)
        
            
        
            # Ajouter un cercle sur la carte
            
            folium.Circle( radius=rayon, location=[lat,lon]).add_to(mapObj)
        
            # Rendre la carte dans un template HTML
            map_html = mapObj._repr_html_()
        else: 
            documents={}
            documents[0]={}
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
            

        donnees1 = db.mission.find({'_id':id})

        donnees2 = list(db.finance.find({'id_mission':id}))
        
        donnees3 = list(db.equipement.find({'id_mission':id}))
        
        donnees4 = list(db.calendrierMission.find({'id_mission':id}))  
        
        poste=verifierSession()
        
        rapports = list(db.rapport.find({"$and": [{'id_mission': id}, {'Destinataire': poste }]}))
        
        if verifierSession() == "Coordonnateur" :
            return render_template('modifierMissionExploration.html',donnees=documents[0], donnees1=donnees1 , donnees2=donnees2 , donnees3=donnees3 , donnees4=donnees4 , list_rapports=rapports ,map_html=map_html , poste ="Coordonnateur" , Type_mission=session['type_mission'] ,chefs=chef,id=id)
        
        
    
    
    if mission['Type'] == "post" :
        
        chef = db.utilisateur.find({
                    "$or": [
                        {"role": "Chef d'équipe"},
                        {"poste": "Responsable de matériel"},
                        {"poste": "Responsable d'etat"}
                    ],
                    "$and": [
                        {"poste": {"$ne": "Coordonnateur"}}
                    ]
                }) 
        
        donnees= db.locatisation.find({ 'id_mission': id })
        
        documents = list(donnees)
        if documents:
            document = documents[0]
            lat = document['lat']
            lon = document['lon']
            rayon = document['rayon']

            mapObj = folium.Map(location=[lat,lon], zoom_start=5)

            # Ajouter la couche de tuiles Esri WorldStreetMap
            tile_layer = folium.raster_layers.TileLayer(
                tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
                attr='Esri',
                name='Esri WorldStreetMap',
                overlay=False,
                control=True
            ).add_to(mapObj)
        
            
        
            # Ajouter un cercle sur la carte
            
            folium.Circle( radius=rayon, location=[lat,lon]).add_to(mapObj)
        
            # Rendre la carte dans un template HTML
            map_html = mapObj._repr_html_()
        else: 
            
            documents={}
            documents[0]={}
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
        
        
        donnees1 = db.mission.find({'_id':id})

        donnees2 = list(db.don.find({'id_mission':id}))
        
        donnees3 = list(db.equipement.find({'id_mission':id}))
        
        donnees4 = list(db.calendrierMission.find({'id_mission':id}))
        
        poste=verifierSession()
        
        rapports = list(db.rapport.find({"$and": [{'id_mission': id}, {'Destinataire': poste }]}))
        
        return render_template('modifierMissionPost.html', donnees=documents[0], donnees1=donnees1 , donnees2=donnees2 , donnees3=donnees3 , donnees4=donnees4 ,map_html=map_html, list_rapports=rapports ,  poste ="Coordonnateur" , Type_mission=session['type_mission'] ,chefs=chef,id=id)
    


@app.route('/update_donnees',methods=['POST'])
def update_donnees() :
    donnees = {}
    if request.method == 'POST':
        id = request.form.get('id')
        chef = db.utilisateur.find({"role":"Chef d'équipe"})

        # Définition des contraintes pour chaque champ
        contraintes = {
            'Nom': lambda valeur: len(valeur) > 0 and len(valeur) <= 50 and bool(re.match('^[a-zA-Z0-9 ]+$', valeur)),
            'Objectif': lambda valeur: len(valeur) > 0 and len(valeur) <= 500 and bool(re.match('^[a-zA-Z0-9 ]+$', valeur)),
            'Date_deb': lambda valeur: len(valeur) > 0 ,
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
    filter = {'_id': id}
    idcoordonnateur = session['utilisateur_id']
    update = { '$set': { 'Nom': nom ,
                         "Objectif": objectif,
                           "Date_deb": date_deb,
                            "Date_fin": date_fin } }
    if not messages_erreur:
        db.mission.update_one(filter, update)
    
 # ----------------------------------------------------------------------------
    donnees_liste = request.form.getlist('table1donnees')
    nb_champs = 4
    nb_lignes = len(donnees_liste) // nb_champs
    lignes = []
    for i in range(nb_lignes):
        ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
        lignes.append(ligne)

    if not messages_erreur:
        for ligne in lignes:
            id2 = ligne[0]
            resultat = db.finance.find_one({"_id": id2})
            if resultat :
                update ={ '$set': { 'Financier': ligne[1],
                                    'budget': ligne[2],
                                    'date_de_financement': ligne[3] } }
                db.finance.update_one(resultat,update)
            else :
                nombre_elements2 = db.finance.count_documents({})
                idFinance = "F" + str(nombre_elements2)
                db.finance.insert_one({"_id": idFinance,
                                    'Financier': ligne[0],
                                    'budget': ligne[2],
                                    'date_de_financement': ligne[3],
                                    'id_mission': id,
                                    "idcoordonnateur": idcoordonnateur})
    ###################################################################
    donnees_liste = request.form.getlist('table2donnees')
    nb_champs = 4
    nb_lignes = len(donnees_liste) // nb_champs
    lignes = []
    for i in range(nb_lignes):
        Ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
        lignes.append(Ligne)

    if not messages_erreur:
        for ligne in lignes:
            id2 = ligne[1]
            resultat = db.equipement.find_one({"_id": id2})
            if resultat :
                update ={ '$set': { 'Nom_equipement': ligne[0],
                                    'quantite': ligne[2],
                                    'equipe': ligne[3] } }
                db.equipement.update_one(resultat,update)
            else :
                nombre_elements2 = db.equipement.count_documents({})
                idEquipement = "EQP" + str(nombre_elements2)
                db.equipement.insert_one({
                    '_id':idEquipement,
                    'Nom_equipement': ligne[0],
                    'quantite': ligne[2],
                    'equipe': ligne[3],
                    'id_mission': id,
                    "idcoordonnateur": idcoordonnateur})
    ######################################################################
    donnees_liste = request.form.getlist('table3donnees')
    nb_champs = 6
    nb_lignes = len(donnees_liste) // nb_champs
    lignes = []
    for i in range(nb_lignes):
        ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
        lignes.append(ligne)

    if not messages_erreur:
        for ligne in lignes:
            id2 = ligne[1]
            resultat = db.calendrierMission.find_one({"_id": id2})
            if resultat :
                update ={'$set': { 'chef_equipe': ligne[0],
                                    'Nom_equipe': ligne[2],
                                    'tache': ligne[3],
                                    'date_debut': ligne[4],
                                    'date_fin': ligne[5] } }
                db.calendrierMission.update_one(resultat,update)
            else:
                nombre_elements3 = db.calendrierMission.count_documents({})
                idEqMission = "EQ" + str(nombre_elements3)

                db.calendrierMission.insert_one({"_id": idEqMission,
                                                'chef_equipe': ligne[0],
                                                'Nom_equipe': ligne[2],
                                                'tache': ligne[3],
                                                'date_debut': ligne[4],
                                                'date_fin': ligne[5],
                                                'id_mission': id,
                                                "idcoordonnateur": idcoordonnateur})
    ###########################################################################################
    
    if 'lat' in session.keys() and 'lon' in session.keys() and 'rayon' in session.keys() and 'id' in session.keys():
        lat = session['lat']
        lon = session['lon']
        rayon = session['rayon']
        id_localisation = session['id']
        
        loc=db.locatisation.find_one({'_id': id_localisation})
        
        if not messages_erreur:
        
            if not loc:
                nombre_elements2 = db.equipement.count_documents({})
                idLocalisation = "Loc" + str(nombre_elements2)
                data = {
                    "_id":idLocalisation,
                    'lat': lat,
                    'lon': lon,
                    'rayon': rayon,
                    'id_mission': id,
                    'idcoordonnateur': idcoordonnateur}
                db.locatisation.insert_one(data)
            
            if  loc:
                filter1 = {'_id': id_localisation}
                update1 ={'$set': { 'lat': lat,
                                    'lon': lon,
                                    'rayon': rayon } }
                db.locatisation.update_one(filter1,update1)
        
        session.pop('lat',None)
        session.pop('lon',None)
        session.pop('rayon',None)   
        
    return redirect(url_for('modifier_mission_exploration', id=id))

            


####################################################################################
####################################################################################

@app.route('/update_donnees_post',methods=['POST'])
def update_donnees_post() :
    donnees = {}
    if request.method == 'POST':
        chef = db.utilisateur.find({"role":"Chef d'équipe"})
        id = request.form.get('id')

        # Définition des contraintes pour chaque champ
        contraintes = {
            'Nom': lambda valeur: len(valeur) > 0 and len(valeur) <= 50 and bool(re.match('^[a-zA-Z0-9 ]+$', valeur)),
            'Objectif': lambda valeur: len(valeur) > 0 and len(valeur) <= 500 and bool(re.match('^[a-zA-Z0-9 ]+$', valeur)),
            'Date_deb': lambda valeur: len(valeur) > 0 ,
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
    filter = {'_id': id}
    idcoordonnateur = session['utilisateur_id']
    update = { '$set': { 'Nom': nom ,
                         "Objectif": objectif,
                           "Date_deb": date_deb,
                            "Date_fin": date_fin } }
    if not messages_erreur:
        db.mission.update_one(filter, update)
    
 # ----------------------------------------------------------------------------
    donnees_liste = request.form.getlist('table1donnees')
    nb_champs = 7
    nb_lignes = len(donnees_liste) // nb_champs
    lignes = []
    for i in range(nb_lignes):
        ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
        lignes.append(ligne)

    if not messages_erreur:
        for ligne in lignes:
            id2 = ligne[0]
            resultat = db.don.find_one({"_id": id2})
            if resultat :
                update ={ '$set': { 'Donnateur': ligne[1],
                                'Type_donnateur': ligne[2],
                                'Telephone': ligne[3],
                                'Type_de_don': ligne[4],
                                'Montant': ligne[5],
                                'Date_don': ligne[6] } }
                db.don.update_one(resultat,update)
            else :
                nombre_elements2 = db.don.count_documents({})
                idDon = "D" + str(nombre_elements2)
                db.don.insert_one({"_id": idDon,
                                'Donnateur': ligne[1],
                                'Type_donnateur': ligne[2],
                                'Telephone': ligne[3],
                                'Type_de_don': ligne[4],
                                'Montant': ligne[5],
                                'Date_don': ligne[6],
                                'id_mission':id,
                                 "idcoordonnateur":idcoordonnateur })
    ###################################################################
    donnees_liste = request.form.getlist('table2donnees')
    nb_champs = 4
    nb_lignes = len(donnees_liste) // nb_champs
    lignes = []
    for i in range(nb_lignes):
        Ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
        lignes.append(Ligne)

    if not messages_erreur:
        for ligne in lignes:
            id2 = ligne[1]
            resultat = db.equipement.find_one({"_id": id2})
            if resultat :
                update ={ '$set': { 'Nom_equipement': ligne[0],
                                    'quantite': ligne[2],
                                    'equipe': ligne[3] } }
                db.equipement.update_one(resultat,update)
            else :
                nombre_elements2 = db.equipement.count_documents({})
                idEquipement = "EQP" + str(nombre_elements2)
                db.equipement.insert_one({
                    '_id':idEquipement,
                    'Nom_equipement': ligne[0],
                    'quantite': ligne[2],
                    'equipe': ligne[3],
                    'id_mission': id,
                    "idcoordonnateur": idcoordonnateur})
    ######################################################################
    donnees_liste = request.form.getlist('table3donnees')
    nb_champs = 6
    nb_lignes = len(donnees_liste) // nb_champs
    lignes = []
    for i in range(nb_lignes):
        ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
        lignes.append(ligne)

    if not messages_erreur:
        for ligne in lignes:
            id2 = ligne[1]
            resultat = db.calendrierMission.find_one({"_id": id2})
            if resultat :
                update ={'$set': { 'chef_equipe': ligne[0],
                                    'Nom_equipe': ligne[2],
                                    'tache': ligne[3],
                                    'date_debut': ligne[4],
                                    'date_fin': ligne[5] } }
                db.calendrierMission.update_one(resultat,update)
            else:
                nombre_elements3 = db.calendrierMission.count_documents({})
                idEqMission = "EQ" + str(nombre_elements3)

                db.calendrierMission.insert_one({"_id": idEqMission,
                                                'chef_equipe': ligne[0],
                                                'Nom_equipe': ligne[2],
                                                'tache': ligne[3],
                                                'date_debut': ligne[4],
                                                'date_fin': ligne[5],
                                                'id_mission': id,
                                                "idcoordonnateur": idcoordonnateur})
 ###########################################################################################
    
    if 'lat' in session.keys() and 'lon' in session.keys() and 'rayon' in session.keys() and 'id' in session.keys():
        lat = session['lat']
        lon = session['lon']
        rayon = session['rayon']
        id_localisation = session['id']
        
        loc=db.locatisation.find_one({'_id': id_localisation})
        
        if not messages_erreur:
        
            if not loc:
                nombre_elements2 = db.equipement.count_documents({})
                idLocalisation = "Loc" + str(nombre_elements2)
                data = {
                    "_id":idLocalisation,
                    'lat': lat,
                    'lon': lon,
                    'rayon': rayon,
                    'id_mission': id,
                    'idcoordonnateur': idcoordonnateur}
                db.locatisation.insert_one(data)
            
            if  loc:
                filter1 = {'_id': id_localisation}
                update1 ={'$set': { 'lat': lat,
                                    'lon': lon,
                                    'rayon': rayon } }
                db.locatisation.update_one(filter1,update1)
           
        session.pop('lat',None)
        session.pop('lon',None)
        session.pop('rayon',None)   
        
    return redirect(url_for('modifier_mission_exploration', id=id))


def verifier_date_fin(date_fin, date_deb):
    if date_fin < date_deb:
        return False
    else:
        return True