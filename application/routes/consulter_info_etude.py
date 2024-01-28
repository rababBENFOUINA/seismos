from application import app
from flask import Flask,Blueprint, render_template, session
from application import db
import folium
from application.routes.acceuil import verifierSession

@app.route('/ConsulterInfoEtude/<id>')
def Consulter_info_etude(id):
   
    donnees= db.locatisation.find({ 'idetude': id })
    documents = list(donnees)
    if documents:
        document = documents[0]
        lat = document['lat']
        lon = document['lon']
        rayon = document['rayon']

        mapObj = folium.Map(location=[lat,lon], zoom_start=5)

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


    donnees1 = db.DonneesEtude.find({'_id':id})

    donnees2 = list(db.CoucheSol.find({'idetude':id}))

    rapports = list(db.rapportEtudeSeisme.find({'idetude': id}))

    if verifierSession() == "Sismologue" :
            return render_template('consulter_info_etude.html',Type_mission=session['type_mission'],donnees=documents, donnees1=donnees1 , donnees2=donnees2 , list_rapports=rapports ,map_html=map_html , poste ="Sismologue" )
    if verifierSession() == "Coordonnateur" :
            return render_template('consulter_info_etude.html',Type_mission=session['type_mission'],donnees=documents, donnees1=donnees1 , donnees2=donnees2 , list_rapports=rapports ,map_html=map_html , poste ="Coordonnateur" )