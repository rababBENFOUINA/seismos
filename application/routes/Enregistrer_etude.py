import re
import folium
from pymongo import MongoClient
from application import db
from application import app
from flask import Flask,Blueprint, render_template, request, session, url_for


@app.route("/EnregistrerEtude")
def Enregistrer_etude():
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
        result = db.mission.find_one({'_id': idmis , 'Type' : "exploration"})
        if result:
            resultats.append(mission)
    return render_template("Enregistrer_etude.html",poste = "Sismologue",Type_mission=session['type_mission'],mission = resultats, map_html=map_html ,messages_erreur=messages_erreur)



######################################################################
######################################################################
@app.route("/EnregistrementEtude",methods=['POST'])
def enregistrer():
    if request.method == 'POST':

        contraintes = {
            'latitude': lambda valeur: len(valeur) > 0 and bool(re.match('^[-+]?([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'longitude': lambda valeur: len(valeur) > 0 and bool(re.match('^[-+]?([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'longueur': lambda valeur: len(valeur) > 0 and bool(re.match('^[-+]?([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'duree_enregistrement': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'nombre_capteur': lambda valeur: len(valeur) > 0 and bool(re.match('^[1-9][0-9]*$', valeur)),
            'distance_capteur': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'energie_source': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'distance_sc': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'profondeur': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'vitesse': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'amplitude': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'temps': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
            'frequence': lambda valeur: len(valeur) > 0 and bool(re.match('^([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur))
        }

        mission = request.form.get('id_mission')
        date = request.form.get('date_etude')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        longueur = request.form.get('longueur')
        methode = request.form.get('methode')
        duree = request.form.get('duree_enregistrement')
        type_capteur = request.form.get('type_capteur')
        nbr_capteur = request.form.get('nombre_capteur')
        distance_capteur = request.form.get('distance_capteur')
        type_source = request.form.get('type_source')
        energie =request.form.get('energie_source')
        distance_sc = request.form.get('distance_sc')
        profodeur_sol =  request.form.get('profondeur')
        vitesse = request.form.get('vitesse')
        amplitude = request.form.get('amplitude')
        temps = request.form.get('temps')
        frequence = request.form.get('frequence')
        idmembre=session['utilisateur_id']

        messages_erreur = {}
        for nom_champ, contrainte in contraintes.items():
            valeur_champ = request.form.get(nom_champ)
            if not contrainte(valeur_champ):
                messages_erreur[nom_champ] = f"Champ invalid"


        nombre_elements = db.DonneesEtude.count_documents({})
        idetude ="E"+ str(nombre_elements)
        if not messages_erreur:
            db.DonneesEtude.insert_one({
                "_id":idetude,
                "idmission": mission,
                "idsismologue":session['utilisateur_id'],
                "date": date,
                "latitude_depart":latitude,
                "longitude_depart":longitude,
                "longueur_profil": longueur,
                "methode_etude": methode,
                "duree_enregistrement":duree,
                "type_capteur":type_capteur,
                "nombre_capteur":nbr_capteur,
                "distance_capteurs":distance_capteur,
                "type_source":type_source,
                "energie_source":energie,
                "distance_source_capteur":distance_sc,
                "profondeur_sol_total":profodeur_sol,
                "vitesse_propagation": vitesse,
                "amplitude_onde_sismique": amplitude,
                "temps_parcours_onde": temps,
                "frequence_onde": frequence
            })

        donnees_liste = request.form.getlist('tabledonnees')
        nb_champs = 4
        nb_lignes = len(donnees_liste) // nb_champs
        lignes = []
        for i in range(nb_lignes):
            ligne = donnees_liste[i*nb_champs: (i+1)*nb_champs]
            lignes.append(ligne)
        if not messages_erreur:
            for ligne in lignes:

                nombre_elements2 = db.CoucheSol.count_documents({})
                idcouche = "CS" + str(nombre_elements2)
                
                db.CoucheSol.insert_one({"_id": idcouche,
                                "idetude":idetude,
                                "idmission": mission,
                                "type_sol":ligne[0],
                                "epaisseur": ligne[1],
                                "profondeur": ligne[2],
                                "vitesse" : ligne[3],
                                "idsismologue":idmembre
                                })
        
        rapportEtudeSeisme = request.files.getlist('rapports')
        if not messages_erreur:
            for  rapport in rapportEtudeSeisme:
                nombre_elements = db.rapportEtudeSeisme.count_documents({})
                idrap= "RE" + str(nombre_elements)
                rapport_data = {
                    '_id': idrap ,
                    'idetude':idetude,
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
                    'idetude': idetude,
                    'idsismologue': idmembre}
                db.locatisation.insert_one(data)
                
                session.pop('lat',None)
                session.pop('lon',None)
                session.pop('rayon',None)

        idmembre=session['utilisateur_id']
        missions = db.affectation.find({"idmembre":idmembre})
        return render_template("Enregistrer_etude.html",poste = "Sismologue",Type_mission=session['type_mission'] ,mission = missions,messages_erreur=messages_erreur, map_html=map_html)
    return render_template("Enregistrer_etude.html",poste = "Sismologue",Type_mission=session['type_mission'],mission = missions,messages_erreur=messages_erreur, map_html=map_html)