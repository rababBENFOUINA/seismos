import re
from bson.binary import Binary
import folium
from application import app
from flask import Flask, Blueprint, render_template, request, session
from pymongo import MongoClient
from application import db
from application.routes.acceuil import verifierSession

@app.route('/consulter_liste_decedes')
def consulter_liste_decedes():
    idU = session['utilisateur_id']
    Info_decedes = db.Info_decedes.find({})
    
    if verifierSession() == "Personnel médical Membre" :
        return render_template("consulter_liste_deces.html" , poste ="Personnel médical Membre" , Info_decedes=Info_decedes )
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("consulter_liste_deces.html" , poste ="Responsable de sécurité Membre" , Info_decedes=Info_decedes )
    
       
   
@app.route('/liste_decedes')
def liste_decedes():
    valeur = request.args.get('valeur')
    idU = session['utilisateur_id']
    Info_decedes = db.Info_decedes.find({"$or": [{"_id": {"$regex": valeur}}, {"id_mission": {"$regex": valeur}}], "idutilisateur": idU})
    
    if verifierSession() == "Personnel médical Membre" :
        return render_template("consulter_liste_deces.html" , poste ="Personnel médical Membre" , Info_decedes=Info_decedes )
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("consulter_liste_deces.html" , poste ="Responsable de sécurité Membre" , Info_decedes=Info_decedes )
    
      
@app.route("/filtrer_liste_decedes")
def filtrer_liste_decedes():
    messages_erreur = {}
    valeur = request.args.get('valeur')
    regex_pattern = re.compile(valeur, re.IGNORECASE)
    
    Info_decedes = db.Info_decedes.find({"$or": [{"_id": {"$regex": regex_pattern}}, {"id_mission": {"$regex": regex_pattern}} ,{"Nom": {"$regex": regex_pattern}},{"Prenom": {"$regex": regex_pattern}},{"CIN": {"$regex": regex_pattern}}]})
    
    if verifierSession() == "Personnel médical Membre" :
        return render_template("consulter_liste_deces.html" , poste ="Personnel médical Membre" , Info_decedes=Info_decedes )
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("consulter_liste_deces.html" , poste ="Responsable de sécurité Membre" , Info_decedes=Info_decedes )
    
       