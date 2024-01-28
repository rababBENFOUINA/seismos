import re
from application import app
from flask import Flask,Blueprint, render_template, request, session 
from pymongo import MongoClient
from application import db
import os

from application.routes.Ajouter_rapport import mission_existe_pas






@app.route("/ajouter_equipement")
def Ajout_materiel():
    messages_erreur = {}
    idmembre=session['utilisateur_id']
    missions=db.calendrierMission.find({'chef_equipe':idmembre})
    return render_template("ajouterMateriel.html",messages_erreur=messages_erreur ,missions=missions, poste ="Responsable de matériel" )




@app.route('/ajouter_equipement', methods=['POST'])
def ajouter_equipement():
    if request.method == 'POST':
        idmembre=session['utilisateur_id']
        missions=db.calendrierMission.find({'chef_equipe':idmembre})
        contraintes = {
            'nom_equipement': lambda valeur: len(valeur) > 0 and len(valeur) <= 100,
            'Poids': lambda valeur: len(valeur) > 0 and bool(re.match('^[-+]?([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),            
            'longueur': lambda valeur: len(valeur) > 0 and bool(re.match('^[-+]?([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),            
            'largeur': lambda valeur: len(valeur) > 0 and bool(re.match('^[-+]?([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),            
            'hauteur': lambda valeur: len(valeur) > 0 and bool(re.match('^[-+]?([0-9]+([.][0-9]*)?|[.][0-9]+)$', valeur)),            

        }
        
        nom_equipement = request.form.get('nom_equipement')
        type_equipement = request.form.get('type_equipement')
        marque_modele = request.form.get('marque_modele')
        Poids = request.form.get('Poids')
        en_service = request.form.get('en_service')
        longueur=request.form.get('longueur')
        largeur=request.form.get('largeur')
        hauteur=request.form.get('hauteur')
        description=request.form.get('description')
        
        messages_erreur = {}
    for nom_champ, contrainte in contraintes.items():
        valeur_champ = request.form.get(nom_champ)
        if not contrainte(valeur_champ):
            messages_erreur[nom_champ] = f"champ invalide"
        
        
        nombre_elements = db.Newequipement.count_documents({})
        idEquipement = "EQ" + str(nombre_elements)
        idresp_materiel = session['utilisateur_id']
        
    if not messages_erreur:    
        info_materiel = {"_id": idEquipement,
                        "nom_equipement": nom_equipement,
                        "type_equipement": type_equipement,
                        "marque_modele": marque_modele,
                        "Poids": Poids, 
                        "en_service": en_service,
                        "longueur": longueur,
                        "largeur": largeur,
                        "hauteur": hauteur,
                        "description" : description,
                        "idressponsableMateriel":idresp_materiel}

        db.Newequipement.insert_one(info_materiel)
        
        
        
        return render_template("ajouterMateriel.html",messages_erreur=messages_erreur ,missions=missions, poste ="Responsable de matériel"  )
    return render_template("ajouterMateriel.html",messages_erreur=messages_erreur ,missions=missions, poste ="Responsable de matériel"  )