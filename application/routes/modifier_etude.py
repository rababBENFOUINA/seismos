import datetime
import re
from tarfile import RECORDSIZE
from application import app
from flask import flash, redirect, render_template,request, session, url_for
from application import db
import folium

from application.routes.acceuil import verifierSession

@app.route("/ModifierEtude/<id>")
def modifier_etude(id):
    messages_erreur = {}
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

    rapports = list(db.rapports.find({'idetude': id}))

    
    return render_template('modifier_etude.html',donnees=documents, donnees1=donnees1 , donnees2=donnees2 , list_rapports=rapports ,map_html=map_html ,poste = "Sismologue",Type_mission=session['type_mission'], messages_erreur=messages_erreur  )
    

@app.route("/modifier_donnees_etude",methods=['POST'])
def modifier_donnees_etude():
    donnees = {}
    if request.method == 'POST':
        contraintes = {
            'latitude': lambda valeur: len(valeur) > 0 and bool(re.match('^[-+]?([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),
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

        id = request.form.get('id')
        
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
                    messages_erreur[nom_champ] = f"Ce champ est invalide"

        

        filter = {'_id': id}

        update = { '$set': { "idmission": mission,
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
                "frequence_onde": frequence } }
        if not messages_erreur:
            db.DonneesEtude.update_one(filter, update)


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
                resultat = db.CoucheSol.find_one({"_id": id2})
                if resultat :
                    update ={ '$set': { "type_sol":ligne[1],
                                    "epaisseur": ligne[2],
                                    "profondeur": ligne[3],
                                    "vitesse" : ligne[4] } }
                    db.CoucheSol.update_one(resultat,update)
                else :
                    nombre_elements2 = db.CoucheSol.count_documents({})
                    idcouche = "CS" + str(nombre_elements2)
                    
                    db.CoucheSol.insert_one({"_id": idcouche,
                                        "idmission": mission,
                                        "idetude":id,
                                    "type_sol":ligne[1],
                                    "epaisseur": ligne[2],
                                    "profondeur": ligne[3],
                                    "vitesse" : ligne[4],
                                    "idsismologue":idmembre
                                    })
        
        #affichage dans meme page
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

        
        return render_template('modifier_etude.html', Type_mission=session['type_mission'], messages_erreur=messages_erreur ,poste = "Sismologue" ,donnees=documents, donnees1=donnees1 , donnees2=donnees2 , list_rapports=rapports ,map_html=map_html )