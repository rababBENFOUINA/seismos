import datetime
import re
import folium
from pymongo import MongoClient
from application import db
from application import app
from flask import Flask,Blueprint, render_template, request, session, url_for


@app.route("/EnregistrerSeisme")
def Enregistrer_seisme():
    messages_erreur = {}
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
    idmembre=session['utilisateur_id']
    resultats = []
    missions = db.affectation.find({"idmembre":idmembre})
    for mission in missions:
        idmis = mission['idmission']
        result = db.mission.find_one({'_id': idmis , 'Type' : "post"})
        if result:
            resultats.append(mission)
    return render_template("Enregistrer_seisme.html",poste = "Sismologue",Type_mission=session['type_mission'],mission = resultats, map_html=map_html,messages_erreur=messages_erreur)


@app.route("/EnregistrerSeisme",methods=['POST'])
def enregistrer_parametre():
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
        nombre_elements = db.ParametreSeisme.count_documents({})
        idseisme ="S"+ str(nombre_elements)
        idmembre=session['utilisateur_id']

        messages_erreur = {}
        for nom_champ, contrainte in contraintes.items():
            valeur_champ = request.form.get(nom_champ)
            if not contrainte(valeur_champ):
                messages_erreur[nom_champ] = f"Champ invalid"

        if not messages_erreur:
            db.ParametreSeisme.insert_one({
                "_id":idseisme,
                "id_mission" : idmission,
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
                "osd": OSD
            })

        donnees_liste = request.form.getlist('table3donnees')
        nb_champs = 4
        nb_lignes = len(donnees_liste) // nb_champs
        lignes = []
        if not messages_erreur:
            for i in range(nb_lignes):
                ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
                lignes.append(ligne)
            for ligne in lignes:

                nombre_elements2 = db.Station.count_documents({})
                idStation = "St" + str(nombre_elements2)
                
                db.Station.insert_one({"_id": idStation,
                                    "idseisme": idseisme,
                                "nom":ligne[0],
                                "distance": ligne[1],
                                "azimut": ligne[2],
                                "amplitude" : ligne[3],
                                'idsismologue': idmembre
                                })
            
        rapportEtudeSeisme = request.files.getlist('rapports')
        if not messages_erreur:
            for  rapport in rapportEtudeSeisme:
                nombre_elements = db.rapportEtudeSeisme.count_documents({})
                idrap= "RS" + str(nombre_elements)
                rapport_data = {
                    '_id': idrap ,
                    'idseisme':idseisme,
                    'nom': rapport.filename,
                    'type': rapport.content_type,
                    'data': rapport.read()
                }
                db.rapportEtudeSeisme.insert_one(rapport_data)
                
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
                
                
                data = {
                    'lat': lat,
                    'lon': lon,
                    'rayon': rayon,
                    'idseisme': idseisme,
                    'idsismologue': idmembre}
                db.locatisation.insert_one(data)
                
                session.pop('lat',None)
                session.pop('lon',None)
                session.pop('rayon',None)
        
        resultats =[]
        idmembre=session['utilisateur_id']
        missions = db.affectation.find({"idmembre":idmembre})
        for mission in missions:
                idmis = mission['idmission']
                result = db.mission.find_one({'_id': idmis , 'Type' : "post"})
                if result:
                    resultats.append(mission)
                    
        return render_template("Enregistrer_seisme.html",poste = "Sismologue",Type_mission=session['type_mission'],mission = resultats,messages_erreur=messages_erreur, map_html=map_html)
    return render_template("Enregistrer_seisme.html",mission = resultats, map_html=map_html,messages_erreur=messages_erreur)