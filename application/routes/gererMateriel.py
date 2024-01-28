from datetime import datetime

from flask_pymongo import DESCENDING
from application import app
from flask import Flask,Blueprint, jsonify, redirect, render_template, request, session, url_for 
from pymongo import MongoClient
from application import db
from application.routes.acceuil import verifierSession


@app.route("/consulterMateriel")
def Gerer_Materiel():
    return render_template("GererMateriel.html")

@app.route("/Consulter_liste_Materiel")
def list_materiel():
    return render_template("GererMateriel.html")

@app.route('/afficher_materiel')
def afficher_materiel():
    # Récupérer les documents de la collection
    materiel = db.Newequipement.find()
    
    # Passer les documents récupérés à la fonction render_template() de Flask
    return render_template('GererMateriel.html', list_materiel=materiel, poste ="Responsable de matériel")

@app.route("/gerer_materiel/<idmis>")
def gerer_materiel(idmis):
    idmis=idmis
    idU = session['utilisateur_id']
    user=db.utilisateur.find_one({"_id":idU})
    materiel=db.afectation_equipement.find({"idmission":idmis , "idchef":idU})
    ids = db.Newequipement.find()
    liste_id = list(ids)
    #return render_template("MembreEquipe.html",list_membre=membres,listes_id=liste_id,idmission=idmis)
    if verifierSession() == "Responsable de matériel" :
        return render_template("MaterielMission.html" , poste="Responsable de matériel"  ,list_materiel=materiel,listes_id=liste_id,idmission=idmis)
    
    
@app.route('/get_equipement', methods=['GET'])
def get_equipement():
    
    id = request.args.get('id')
    
    affect_exist = db.afectation_equipement.count_documents({'id_eq': id })
    
    if affect_exist != 0:
        current_date = datetime.now().strftime("%Y-%m-%d")
        affectation = db.afectation_equipement.find_one({'id_eq': id}, sort=[('date_debut', DESCENDING)])

        if affectation and affectation['date_fin'] > current_date:
            return jsonify({'id_affect':affectation['_id'] ,'nom': affectation['nom'], 'date_debut': affectation['date_debut'], 'date_fin': affectation['date_fin']})

        else:
            eq = db.Newequipement.find_one({'_id': id})
            return jsonify({'nom': eq['nom_equipement'], 'date_debut': "", 'date_fin': ""})

    else:
        eq = db.Newequipement.find_one({'_id': id})
        return jsonify({'nom': eq['nom_equipement'], 'date_debut': "", 'date_fin': ""})
  
  
@app.route("/Affecterequipement", methods=['POST'])
def Affecterequipement():
    id = request.form.get('id')
    id_aff = request.form.get('id_aff')
    nom = request.form.get('nom')
    date_debut = request.form.get('date_deb')
    date_fin = request.form.get('date_fin')
    mission = request.form.get('idmission')
    idU = session['utilisateur_id']

    current_date = datetime.now().strftime("%Y-%m-%d")

    affect_exist = db.afectation_equipement.count_documents({'id_eq': id })
    if affect_exist == 0:
        
        nombre_affect = db.afectation_equipement.count_documents({})

        id_affect = "AfEq" + str(nombre_affect)

        infos_membre = {
            "_id": id_affect,
            "id_eq": id,
            "nom": nom,
            "date_debut": date_debut,
            "date_fin": date_fin,
            "idchef": idU,
            "idmission": mission
        }
        db.afectation_equipement.insert_one(infos_membre)
    else:
        affectation = db.afectation_equipement.find_one({'id_eq': id}, sort=[('date_debut', DESCENDING)])
        if affectation['date_fin'] < current_date:
            nombre_affect = db.afectation_equipement.count_documents({})

            id_affect = "AfEq" + str(nombre_affect)

            infos_membre = {
                "_id": id_affect,
                "id_eq": id,
                "nom": nom,
                "date_debut": date_debut,
                "date_fin": date_fin,
                "idchef": idU,
                "idmission": mission
            }
            db.afectation_equipement.insert_one(infos_membre)
        else :     
            infos_membre2 = {
                "id_eq": id,
                "nom": nom,
                "date_debut": date_debut,
                "date_fin": date_fin,
                "idchef": idU,
                "idmission": mission
            }
            db.afectation_equipement.update_one({'_id': id_aff}, {'$set': infos_membre2})

    return redirect(url_for('gerer_materiel'))    