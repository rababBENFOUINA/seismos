import re
from bson.binary import Binary
import folium
from application import app
from flask import Flask, Blueprint, render_template, request, session
from pymongo import MongoClient
from application import db
from application.routes.acceuil import verifierSession

@app.route('/consulter_liste_intervenant')
def consulter_liste_intervenant():
    idU = session['utilisateur_id']
    Info_intervenant = db.Intervenant.find({})
    return render_template("consulter_liste_intervenant.html" , poste ="Responsable de sécurité Membre" , Info_intervenant = Info_intervenant )
    
@app.route("/filtrer_liste_intervenant")
def filtrer_liste_intervenant():
    messages_erreur = {}
    valeur = request.args.get('valeur')
    Info_intervenant = db.Intervenant.find({"$or": [{"_id": {"$regex": valeur}}, {"id_mission": {"$regex": valeur}}, {"Role": {"$regex": valeur}},{"Nom": {"$regex": valeur}},{"Prenom": {"$regex": valeur}},{"CIN": {"$regex": valeur}}]})
    return render_template("consulter_liste_intervenant.html" , poste ="Personnel médical Membre" , Info_intervenant=Info_intervenant )
    
@app.route("/ConsulterInfoIntrvenant/<id>")
def ConsulterInfoIntrvenant(id):
    infoIntervenant = db.Intervenant.find({"_id":id})    
    return render_template('consulter_info_intervenant.html', poste ="Personnel médical Membre" , Info_intervenant=infoIntervenant)