import re
from bson.binary import Binary
import folium
from application import app
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from application import db
from application.routes.acceuil import verifierSession

@app.route('/consulter_liste_patients')
def consulter_liste_patients():
    idU = session['utilisateur_id']
    info_patient = db.Info_patient.find({})
    
    if verifierSession() == "Personnel médical Membre" :
        return render_template("consulter_liste_patients.html" , poste ="Personnel médical Membre" , info_patient=info_patient )
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("consulter_liste_patients.html" , poste ="Responsable de sécurité Membre" , info_patient=info_patient )
    
       
   
@app.route('/liste_patients')
def liste_patients():
    valeur = request.args.get('valeur')
    idU = session['utilisateur_id']
    info_patient = db.Info_patient.find({"$or": [{"_id": {"$regex": valeur}}, {"id_mission": {"$regex": valeur}}], "idutilisateur": idU})
    
    if verifierSession() == "Personnel médical Membre" :
        return render_template("consulter_liste_patients.html" , poste ="Personnel médical Membre" , info_patient=info_patient )
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("consulter_liste_patients.html" , poste ="Responsable de sécurité Membre" , info_patient=info_patient )
    
      
@app.route("/filtrer_liste_patients")
def filtrer_liste_patients():
    messages_erreur = {}
    valeur = request.args.get('valeur')
    regex_pattern = re.compile(valeur, re.IGNORECASE)
    info_patient = db.Info_patient.find({"$or": [{"_id": {"$regex": regex_pattern}}, {"id_mission": {"$regex": regex_pattern}} ,{"Nom": {"$regex": regex_pattern}},{"Prenom": {"$regex": regex_pattern}},{"CIN": {"$regex": regex_pattern}}]})
    
    if verifierSession() == "Personnel médical Membre" :
        return render_template("consulter_liste_patients.html" , poste ="Personnel médical Membre" , info_patient=info_patient )
    if verifierSession() == "Responsable de sécurité Membre" :
        return render_template("consulter_liste_patients.html" , poste ="Responsable de sécurité Membre" , info_patient=info_patient )
    
       