import datetime
import re
from tarfile import RECORDSIZE
from application import app
from flask import flash, redirect, render_template,request, session, url_for
from application import db
import folium

from application.routes.acceuil import verifierSession

@app.route("/ModifierSeisme/<id>")
def modifier_seisme(id):
    messages_erreur = {}
    donnees= db.locatisation.find({ 'idseisme': id })
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


    donnees1 = db.ParametreSeisme.find({'_id':id})

    donnees2 = list(db.Station.find({'idseisme':id}))

    rapports = list(db.rapports.find({'idseisme': id}))

    
    return render_template('modifier_seisme.html',donnees=documents, donnees1=donnees1 , donnees2=donnees2 , list_rapports=rapports ,map_html=map_html ,poste = "Sismologue",Type_mission=session['type_mission'], messages_erreur=messages_erreur  )
    

@app.route("/modifier_donnees_seisme",methods=['POST'])
def modifier_donnees_seisme():
    donnees = {}
    if request.method == 'POST':
        contraintes = {
            'date_seisme': lambda valeur: len(valeur) > 0 and datetime.datetime.strptime(valeur, '%Y-%m-%d') <= datetime.datetime.now(),
            'heure_seisme': lambda valeur: len(valeur) > 0,
            'duree': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'latitude': lambda valeur: len(valeur) > 0 and bool(re.match('^[-+]?([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'longitude': lambda valeur: len(valeur) > 0 and bool(re.match('^[-+]?([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'profondeur': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'magnitude': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'erreur_magnitude': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'Onde_P_crete': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'Onde_S_crete': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'Onde_P_vitesse': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'Onde_S_vitesse': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'Onde_P_deplacement': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'Onde_S_deplacement': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),

        }

        idmission = request.form.get('id_mission')
        typeseisme = request.form.get('type_seisme')
        dateseisme = request.form.get('date_seisme')
        heureseisme = request.form.get('heure_seisme')
        duree = request.form.get('duree')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        profondeur = request.form.get('profondeur')
        magnitude = request.form.get('magnitude')
        magType = request.form.get('type_magnitude') 
        magErreur = request.form.get('erreur_magnitude')
        OPC =  request.form.get('Onde_P_crete')
        OSC = request.form.get('Onde_S_crete')
        OPV = request.form.get('Onde_P_vitesse')
        OSV = request.form.get('Onde_S_vitesse')
        OPD = request.form.get('Onde_P_deplacement')
        OSD = request.form.get('Onde_S_deplacement')
        idmembre=session['utilisateur_id']
        id = request.form.get('id')


        messages_erreur = {}
        for nom_champ, contrainte in contraintes.items():
                valeur_champ = request.form.get(nom_champ)
                if not contrainte(valeur_champ):
                    messages_erreur[nom_champ] = f"champ invalide"

        

        filter = {'_id': id}

        update = { '$set': { "id_mission" : idmission,
                "type_seisme" : typeseisme,
                "date_seisme" : dateseisme,
                "heure_seisme" : heureseisme,
                "duree" : duree,
                "idsismologue":session['utilisateur_id'],
                "latitude":latitude,
                "longitude": longitude,
                "profondeur": profondeur,
                "magnitude": magnitude,
                "magtype": magType,
                "magerreur": magErreur,
                "opc": OPC,
                "osc": OSC,
                "opv": OPV,
                "osv": OSV,
                "opd": OPD,
                "osd": OSD } }
        if not messages_erreur:
            db.ParametreSeisme.update_one(filter, update)


        donnees_liste = request.form.getlist('tabledonnees')
        nb_champs = 5
        nb_lignes = len(donnees_liste) // nb_champs
        lignes = []
        for i in range(nb_lignes):
            ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
            lignes.append(ligne)

        if not messages_erreur:
            for ligne in lignes:
                id2 = ligne[0]
                resultat = db.Station.find_one({"_id": id2})
                if resultat :
                    update ={ '$set': { "nom":ligne[1],
                                "distance": ligne[2],
                                "azimut": ligne[3],
                                "amplitude" : ligne[4] } }
                    db.Station.update_one(resultat,update)
                else :
                    nombre_elements2 = db.Station.count_documents({})
                    idStation = "St" + str(nombre_elements2)
                    
                    db.Station.insert_one({"_id": idStation,
                                "idseisme": id,
                                "nom":ligne[1],
                                "distance": ligne[2],
                                "azimut": ligne[3],
                                "amplitude" : ligne[4],
                                'idsismologue': idmembre
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
        if not messages_erreur:
            if 'lat' in session.keys() and 'lon' in session.keys() and 'rayon' in session.keys():
                lat = session['lat']
                lon = session['lon']
                rayon = session['rayon']
                
                donnees= db.locatisation.find({ 'idseisme': id })
                documents = list(donnees)
                if documents:
                    update ={ '$set': { 'lat': lat,
                        'lon': lon,
                        'rayon': rayon,
                        'idseisme': idseisme,
                        'idsismologue': idmembre } }
                    db.locatisation.update_one({'_id':documents[0]},update)
               


        donnees= db.locatisation.find({ 'idseisme': id })
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


        donnees1 = db.ParametreSeisme.find({'_id':id})

        donnees2 = list(db.Station.find({'idseisme':id}))

        rapports = list(db.rapports.find({'idseisme': id}))

        return render_template("modifier_seisme.html" , Type_mission=session['type_mission'], messages_erreur=messages_erreur , poste ="Sismologue"  ,donnees=documents, donnees1=donnees1 , donnees2=donnees2,map_html=map_html)