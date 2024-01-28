import re
from flask import Flask, redirect, render_template, request, session, url_for
import folium
from application import app
from application import db
from application.routes.acceuil import verifierSession

@app.route("/map", methods=['POST'])
def mymap():
    
    
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
    messages_erreur = request.args.get("messages_erreur")
    
    resultats = []
    idmembre=session['utilisateur_id']
    missions = db.affectation.find({"idmembre":idmembre})
    for mission in missions:
                idmis = mission['idmission']
                result = db.mission.find_one({'_id': idmis , 'Type' : "exploration"})
                if result:
                    resultats.append(mission)

    
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    rayon = request.form.get('rayon')
    id = request.form.get('id_localisation')
    page = request.form.get('page')
    id_mission = request.form.get('id_mission')
    
    donnees = {
                'lat': lat,
                'lon': lon,
                'rayon': rayon}
    

    
    if lat and lon and rayon : 
        session['lat'] = lat
        session['lon'] = lon
        session['rayon'] = rayon
        session['id'] = id
    
    
  
    # Créer la carte  
    if lat and lon and rayon  and  re.match('^[-]?\d+(\.\d+)?$', lat) and  re.match('^[-]?\d+(\.\d+)?$', lon) and re.match("^[0-9.]+$", rayon) :  
        mapObj = folium.Map(location=[lat, lon], zoom_start=5)

        # Ajouter la couche de tuiles Esri WorldStreetMap
        tile_layer = folium.raster_layers.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Esri WorldStreetMap',
            overlay=False,
            control=True
        ).add_to(mapObj)
    
    
        # Ajouter un cercle sur la carte
        folium.Circle(radius=rayon, location=[lat, lon]).add_to(mapObj)
    
        # Rendre la carte dans un template HTML
        map_html = mapObj._repr_html_()
        
        
        if verifierSession() == "Coordonnateur" and page == "ajout" :
            return render_template("CreeMissionExploration.html" , poste ="Coordonnateur" , messages_erreur=messages_erreur ,chef=chef, map_html=map_html,donnee=donnees , Type_mission=session['type_mission'])
        if verifierSession() == "Responsable de matériel" and page == "ajout"  :
            return render_template("CreeMissionExploration.html" , poste ="Responsable de matériel" , messages_erreur=messages_erreur ,chef=chef, map_html=map_html,donnee=donnees)
        if verifierSession() == "Sismologue"   :
            return render_template("Enregistrer_etude.html" ,mission=resultats, poste ="Sismologue" , messages_erreur=messages_erreur ,chef=chef, map_html=map_html,donnee=donnees,Type_mission=session['type_mission'])
        
        
        if verifierSession() == "Coordonnateur" and page == "modification" :
            
            donnees1 = db.mission.find({'_id':id_mission})

            donnees2 = list(db.finance.find({'id_mission':id_mission}))
            
            donnees3 = list(db.equipement.find({'id_mission':id_mission}))
            
            donnees4 = list(db.calendrierMission.find({'id_mission':id_mission}))
            
            poste=verifierSession()
            
            rapports = list(db.rapport.find({"$and": [{'id_mission': id_mission}, {'Destinataire': poste }]}))
            
        
            return render_template('modifierMissionExploration.html',donnees=donnees, donnees1=donnees1 , donnees2=donnees2 , donnees3=donnees3 , donnees4=donnees4 , list_rapports=rapports ,map_html=map_html , poste ="Coordonnateur" , Type_mission=session['type_mission'],id=id_mission)
        
        if verifierSession() == "Responsable de matériel" and page == "modification"  :
            return render_template("modifierMissionExploration.html" , poste ="Responsable de matériel" , messages_erreur=messages_erreur ,chef=chef, map_html=map_html,donnee=donnees)
 
 
    else :
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
            return render_template("CreeMissionExploration.html" , poste ="Coordonnateur" ,chef=chef, messages_erreur=messages_erreur , map_html=map_html,donnee=donnees , Type_mission=session['type_mission'])
        if verifierSession() == "Responsable de matériel" :
            return render_template("CreeMissionExploration.html" , poste ="Responsable de matériel" ,chef=chef, messages_erreur=messages_erreur , map_html=map_html,donnee=donnees ,Type_mission=session['type_mission'])
        
 
 




@app.route("/mapPost", methods=['POST'])
def mymapPost():
    resultats = []
    messages_erreur = request.args.get("messages_erreur")
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

    lat = request.form.get('lat')
    lon = request.form.get('lon')
    rayon = request.form.get('rayon')
    id = request.form.get('id_localisation')
    page = request.form.get('page')
    id_mission = request.form.get('id_mission')
    
            
    idmembre=session['utilisateur_id']
    missions = db.affectation.find({"idmembre":idmembre})
    for mission in missions:
                idmis = mission['idmission']
                result = db.mission.find_one({'_id': idmis , 'Type' : "post"})
                if result:
                    resultats.append(mission)
    
    donnees = {
                "lat": lat,
                "lon": lon,
                "rayon": rayon}

   
    if lat and lon and rayon : 
        session['lat'] = lat
        session['lon'] = lon
        session['rayon'] = rayon
        session['id'] = id
    
    
  
    # Créer la carte  
    if lat and lon and rayon  and  re.match('^[-]?\d+(\.\d+)?$', lat) and  re.match('^[-]?\d+(\.\d+)?$', lon) and re.match("^[0-9.]+$", rayon) :  
        mapObj = folium.Map(location=[lat, lon], zoom_start=5)

        # Ajouter la couche de tuiles Esri WorldStreetMap
        tile_layer = folium.raster_layers.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Esri WorldStreetMap',
            overlay=False,
            control=True
        ).add_to(mapObj)
    
    
        # Ajouter un cercle sur la carte
        folium.Circle(radius=rayon, location=[lat, lon]).add_to(mapObj)
    
        # Rendre la carte dans un template HTML
        map_html = mapObj._repr_html_()
        
        if verifierSession() == "Coordonnateur" and page == "ajout" :
            return render_template("CreeMissionPost.html" , poste ="Coordonnateur" , messages_erreur=messages_erreur ,chef=chef, map_html=map_html,donnee=donnees , Type_mission=session['type_mission'])
        if verifierSession() == "Responsable de matériel" and page == "ajout"  :
            return render_template("CreeMissionPost.html" , poste ="Responsable de matériel" , messages_erreur=messages_erreur ,chef=chef, map_html=map_html,donnee=donnees)
        if verifierSession() == "Sismologue"   :
            return render_template("Enregistrer_seisme.html" ,mission=resultats, poste ="Sismologue" , messages_erreur=messages_erreur ,chef=chef, map_html=map_html,donnee=donnees,Type_mission=session['type_mission'])

        
        if verifierSession() == "Coordonnateur" and page == "modification" :
            
            donnees1 = db.mission.find({'_id':id_mission})

            donnees2 = list(db.don.find({'id_mission':id_mission}))
            
            donnees3 = list(db.equipement.find({'id_mission':id_mission}))
            
            donnees4 = list(db.calendrierMission.find({'id_mission':id_mission}))
            
            poste=verifierSession()
            
            rapports = list(db.rapport.find({"$and": [{'id_mission': id_mission}, {'Destinataire': poste }]}))
            
            
            return render_template('modifierMissionPost.html',donnees=donnees, donnees1=donnees1 , donnees2=donnees2 , donnees3=donnees3 , donnees4=donnees4 , list_rapports=rapports ,map_html=map_html , poste ="Coordonnateur" , Type_mission=session['type_mission'],id=id_mission)
        
        if verifierSession() == "Responsable de matériel" and page == "modification"  :
            return render_template("modifierMissionPost.html" , poste ="Responsable de matériel" , messages_erreur=messages_erreur ,chef=chef, map_html=map_html,donnee=donnees)
 
 
    
    else :
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
            return render_template("CreeMissionPost.html" , poste ="Coordonnateur" , messages_erreur=messages_erreur ,chef=chef, map_html=map_html,donnee=donnees , Type_mission=session['type_mission'])
        if verifierSession() == "Responsable de matériel" :
            return render_template("CreeMissionPost.html" , poste ="Responsable de matériel" , messages_erreur=messages_erreur ,chef=chef, map_html=map_html,donnee=donnees)
 




