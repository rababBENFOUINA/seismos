import re
from bson.binary import Binary
import folium
from application import app
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from application import db
from application.routes.acceuil import verifierSession

@app.route('/consulter_liste_seisme')
def consulter_liste_seisme():
    idU = session['utilisateur_id']
    info_user = db.utilisateur.find_one({'_id': idU})
    
    info_seisme = db.ParametreSeisme.find({'idsismologue': info_user['_id']})
    
    return render_template("consulter_liste_seisme.html",poste = "Sismologue",Type_mission=session['type_mission'], info_seismes=info_seisme)


@app.route("/filtrer_Liste_seisme")
def filtrer_Liste_seisme():
    messages_erreur = {}
    idU = session['utilisateur_id']
    info_user = db.utilisateur.find_one({'_id': idU})
    
    valeur = request.args.get('valeur')
    regex_pattern = re.compile(valeur, re.IGNORECASE)
    
    
    info_seisme = db.ParametreSeisme.find({
        "$and": [
            {'idsismologue': info_user['_id']},
            {'$or': [{"_id": {"$regex": regex_pattern}}, {"type_seisme": {"$regex": regex_pattern}}, {"date_seisme": {"$regex": regex_pattern}}]}
            ]
        })
    return render_template("consulter_liste_seisme.html",poste = "Sismologue",Type_mission=session['type_mission'], info_seismes=info_seisme)
    
  