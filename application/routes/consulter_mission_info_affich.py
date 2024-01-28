from application import app
from flask import Flask,Blueprint, render_template, session
from application import db
import folium

from application.routes.acceuil import verifierSession


@app.route('/afficher_info_mission/<id>')
def afficher_donnee(id):
    mission = db.mission.find_one({'_id':id})
    if mission['Type'] == "exploration" :
        
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
        
       
        info_etude = db.DonneesEtude.find({'idmission': id})
        
        if verifierSession() == "Coordonnateur" :
            return render_template('consulter_mission_info_affich.html',donnees=documents, donnees1=donnees1 , donnees2=donnees2 , donnees3=donnees3 , donnees4=donnees4 , list_rapports=rapports ,map_html=map_html , poste ="Coordonnateur" , Type_mission=session['type_mission'],info_etudes=info_etude)
        if verifierSession() == "Responsable de matériel" :
            return render_template('consulter_mission_info_affich.html',donnees=documents, donnees1=donnees1 , donnees2=donnees2 , donnees3=donnees3 , donnees4=donnees4, list_rapports=rapports , map_html=map_html , poste ="Responsable de matériel" , Type_mission=session['type_mission'],info_etudes=info_etude)
        if verifierSession() == "chef" :
            return render_template("consulter_mission_info_affich.html",donnees=documents, donnees1=donnees1 , donnees2=donnees2 , donnees3=donnees3 , donnees4=donnees4, list_rapports=rapports , map_html=map_html , role="chef" , Type_mission=session['type_mission'],info_etudes=info_etude)
        if verifierSession() == "Personnel médical Chef" :
            return render_template("consulter_mission_info_affich.html", role="Personnel médical Chef", donnees1=donnees1 , donnees2=donnees2 , donnees3=donnees3 , donnees4=donnees4, list_rapports=rapports , map_html=map_html , Type_mission=session['type_mission'],info_etudes=info_etude)
    
    
    if mission['Type'] == "post" :
        
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

        info_seisme = db.ParametreSeisme.find({'id_mission': id})
        
        if verifierSession() == "Coordonnateur" :
            return render_template('consulter_mission_post_info_affich.html',donnees=documents, donnees1=donnees1 , donnees2=donnees2 , donnees3=donnees3 , donnees4=donnees4 , list_rapports=rapports, map_html=map_html , poste ="Coordonnateur", Type_mission=session['type_mission'] , info_seismes=info_seisme)
        if verifierSession() == "Responsable de matériel" :
            return render_template('consulter_mission_post_info_affich.html',donnees=documents, donnees1=donnees1 , donnees2=donnees2 , donnees3=donnees3 , donnees4=donnees4 , list_rapports=rapports, map_html=map_html , poste ="Responsable de matériel" , Type_mission=session['type_mission'])
        if verifierSession() == "chef" :
            return render_template("consulter_mission_post_info_affich.html",donnees=documents, donnees1=donnees1 , donnees2=donnees2 , donnees3=donnees3 , donnees4=donnees4, list_rapports=rapports , map_html=map_html , role="chef" , Type_mission=session['type_mission'])
        if verifierSession() == "Personnel médical Chef" :
            return render_template("consulter_mission_post_info_affich.html", role="Personnel médical Chef", donnees1=donnees1 , donnees2=donnees2 , donnees3=donnees3 , donnees4=donnees4, list_rapports=rapports , map_html=map_html , Type_mission=session['type_mission'])
    
    
        
        
def verifierPosteUtilisateur(id_mission):
    missions = db.mission.find({"_id": id_mission})
    id_user = missions.get("utilisateur")
    user = db.utilisateur.find({"_id" : id_user})
    return user("poste")


