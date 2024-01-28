
from datetime import datetime
from flask_pymongo import DESCENDING
from application import app
from application import db
from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from application.routes.acceuil import verifierSession


@app.route("/GererEquipe")
def gerer_equipe():
    if verifierSession() == "Coordonnateur" :
        return render_template("GererEquipe.html" , poste ="Coordonnateur")
    if verifierSession() == "Responsable de matériel" :
        return render_template("GererEquipe.html" , poste ="Responsable de matériel")
    


@app.route("/AfficherChef")
def afficher_equipe():
    
    idU = session['utilisateur_id']
    
    if verifierSession() == "Coordonnateur" :
        Menmbre = db.utilisateur.find().sort("poste")
    else :     
        Menmbre = db.utilisateur.find({"role":"Membre","idutilisateur":idU})

    if verifierSession() == "Coordonnateur" :
        return render_template("GererEquipe.html" , poste ="Coordonnateur", list_chef=Menmbre , Type_mission=session['type_mission'])
    if verifierSession() == "Responsable de matériel" :
        return render_template("GererEquipe.html" , poste ="Responsable de matériel", list_chef=Menmbre)
    if verifierSession() == "chef" :
        return render_template("GererEquipe.html" , role="chef" , list_chef=Menmbre)
    if verifierSession() == "Personnel médical Chef" :
        return render_template("GererEquipe.html" , role="Personnel médical Chef" , list_chef=Menmbre)
  
  
    
##################################  Gestion partie des chefs  #########################################################
@app.route("/GererMembre/<idm>/<idc>")
def gerer_membre(idm,idc):
    idmis=idm
    idU = session['utilisateur_id']
    user=db.utilisateur.find_one({"_id":idU})
    membres = db.affectation.find({"idmission":idmis , "idchef":idc})
    ids = db.utilisateur.find({"role":"Membre" , "poste":user['poste']})
    liste_id = list(ids)
    #return render_template("MembreEquipe.html",list_membre=membres,listes_id=liste_id,idmission=idmis)
    if verifierSession() == "chef" :
        return render_template("MembreEquipe.html" , role="chef"  ,list_membre=membres,listes_id=liste_id,idmission=idmis)
    if verifierSession() == "Personnel médical Chef" :
        return render_template("MembreEquipe.html" , role="Personnel médical Chef" ,list_membre=membres,listes_id=liste_id,idmission=idmis)
  

@app.route('/get_member', methods=['GET'])
def get_member():
    
    id = request.args.get('id')
    
    affect_exist = db.affectation.count_documents({'idmembre': id })
    
    if affect_exist != 0:
        current_date = datetime.now().strftime("%Y-%m-%d")
        affectation = db.affectation.find_one({'idmembre': id}, sort=[('date_debut', DESCENDING)])

        if affectation and affectation['date_fin'] > current_date:
            return jsonify({'id_affect':affectation['_id'] ,'nom': affectation['nom'], 'prenom': affectation['prenom'], 'date_debut': affectation['date_debut'], 'date_fin': affectation['date_fin'], 'tache': affectation['tache']})

        else:
            member2 = db.utilisateur.find_one({'_id': id})
            return jsonify({'nom': member2['Nom'], 'prenom': member2['Prenom'], 'date_debut': "", 'date_fin': "", 'tache': ""})

    else:
        member2 = db.utilisateur.find_one({'_id': id})
        return jsonify({'nom': member2['Nom'], 'prenom': member2['Prenom'], 'date_debut': "", 'date_fin': "", 'tache': ""})


    
    

@app.route("/AffecterTache", methods=['POST'])
def AffecterTache():
    id = request.form.get('id')
    id_aff = request.form.get('id_aff')
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    date_debut = request.form.get('date_deb')
    date_fin = request.form.get('date_fin')
    tache = request.form.get('tache')
    chef = request.form.get('idchef')
    mission = request.form.get('idmission')

    affect_exist = db.affectation.count_documents({'idmembre': id })
    eq=db.affectation.find_one({'idmembre': id })
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    if affect_exist == 0 :
        nombre_affect = db.affectation.count_documents({})

        id_affect = "Af" + str(nombre_affect)

        infos_membre = {
            "_id": id_affect,
            "idmembre": id,
            "nom": nom,
            "prenom": prenom,
            "date_debut": date_debut,
            "date_fin": date_fin,
            "tache": tache,
            "idchef": chef,
            "idmission": mission
        }
        db.affectation.insert_one(infos_membre)
    else:
        affectation = db.affectation.find_one({'idmembre': id}, sort=[('date_fin', DESCENDING)])
        if affectation['date_fin'] < current_date:
            nombre_affect = db.affectation.count_documents({})

            id_affect = "Af" + str(nombre_affect)

            infos_membre = {
                "_id": id_affect,
                "idmembre": id,
                "nom": nom,
                "prenom": prenom,
                "date_debut": date_debut,
                "date_fin": date_fin,
                "tache": tache,
                "idchef": chef,
                "idmission": mission
            }
            db.affectation.insert_one(infos_membre)
        else : 
            infos_membre2 = {
                "idmembre": id,
                "nom": nom,
                "prenom": prenom,
                "date_debut": date_debut,
                "date_fin": date_fin,
                "tache": tache,
                "idchef": chef,
                "idmission": mission
            }
            db.affectation.update_one({'_id': id_aff}, {'$set': infos_membre2})

    return redirect(url_for('gerer_membre'))
 


#@app.route('/supp_affectation/<id>/<mission>')
#def supp_affectation(id, mission):
    #idU = session['utilisateur_id']
    #db.affectation.delete_one({"idmembre": id, "idmission": mission, "idchef": idU})
    #return redirect(url_for('gerer_membre', idm=mission, idc=idU))
