import re
from application import app
from flask import Flask, Blueprint, render_template, request, session
from application import db
from application.routes.acceuil import verifierSession


@app.route("/Consulter_informations_mission")
def list_missions():
    return render_template("consulter_missions.html")


@app.route('/afficher_mission')
def afficher_mission():

    idU = session['utilisateur_id']
    info_user = db.utilisateur.find_one({'_id': idU})
    

    document_exploration=[]
    document_post=[]
    
    if info_user and info_user.get('poste') == 'Coordonnateur':
        donnees_ex = db.mission.find({'idcoordonnateur': info_user['_id'] , 'Type': 'exploration'})
        document_exploration = list(donnees_ex)
        
        donnees_post = db.mission.find({'idcoordonnateur': info_user['_id'] , 'Type': 'post'})
        document_post = list(donnees_post)
    else:
        if session['type_mission']=="exploration" :
            missions = db.mission.find({'Type': 'exploration'}) 
            doc_mission = list(missions)

            for mis in doc_mission:
                id_mission = mis['_id']
                X = db.calendrierMission.count_documents(
                    {'id_mission': id_mission, 'chef_equipe': idU} )

                if X != 0:
                    document_exploration.append(mis)
        
        if session['type_mission']=="post" :            
            missions = db.mission.find({'Type': 'post'}) 
            doc_mission = list(missions)

            for mis in doc_mission:
                id_mission = mis['_id']
                X = db.calendrierMission.count_documents(
                    {'id_mission': id_mission, 'chef_equipe': idU})

                if X != 0:
                    document_post.append(mis)


        # Passer les documents récupérés à la fonction render_template() de Flask
    if verifierSession() == "Coordonnateur" and session['type_mission']=="exploration" :
        return render_template("consulter_missions.html", poste="Coordonnateur", list_missions=document_exploration , Type_mission=session['type_mission'])
    if verifierSession() == "Coordonnateur" and session['type_mission']=="post":
        return render_template("consulter_missions.html", poste="Coordonnateur", list_missions=document_post , Type_mission=session['type_mission'])
    
    if verifierSession() == "Responsable de matériel" and session['type_mission']=="exploration" :
        return render_template("consulter_missions.html", poste="Responsable de matériel", list_missions=document_exploration , Type_mission=session['type_mission'])
    if verifierSession() == "Responsable de matériel" and session['type_mission']=="post":
        return render_template("consulter_missions.html", poste="Responsable de matériel", list_missions=document_post , Type_mission=session['type_mission'])
    
    if verifierSession() == "chef" and session['type_mission']=="exploration":
        return render_template("consulter_missions.html", role="chef", list_missions=document_exploration , Type_mission=session['type_mission'])
    if verifierSession() == "chef" and session['type_mission']=="post":
        return render_template("consulter_missions.html", role="chef", list_missions=document_post , Type_mission=session['type_mission'])
    
    if verifierSession() == "Personnel médical Chef" and session['type_mission']=="exploration":
        return render_template("consulter_missions.html", poste="Personnel médical Chef", list_missions=document_exploration , Type_mission=session['type_mission'])
    if verifierSession() == "Personnel médical Chef" and session['type_mission']=="post":
        return render_template("consulter_missions.html", poste="Personnel médical Chef", list_missions=document_post , Type_mission=session['type_mission'])
  
    
@app.route("/filtrer_liste_mission")
def filtrer_liste_mission():
    messages_erreur = {}
    valeur = request.args.get('valeur')
    regex_pattern = re.compile(valeur, re.IGNORECASE)
    #info_patient = db.Info_patient.find({"$or": [{"_id": {"$regex": valeur}}, {"id_mission": {"$regex": valeur}} ,{"Nom": {"$regex": valeur}},{"Prenom": {"$regex": valeur}},{"CIN": {"$regex": valeur}}]})
    
    
    idU = session['utilisateur_id']
    info_user = db.utilisateur.find_one({'_id': idU})

    document_exploration=[]
    document_post=[]
    
    if info_user and info_user.get('poste') == 'Coordonnateur':
        donnees_ex = db.mission.find({
        "$and": [
            {'idcoordonnateur': info_user['_id']},
            {'Type': 'exploration'},
            {'$or': [{"_id": {"$regex": regex_pattern}}, {"Nom": {"$regex": regex_pattern}}, {"Objectif": {"$regex": regex_pattern}}, {"Type": {"$regex": regex_pattern}}, {"Date_deb": {"$regex": regex_pattern}}, {"Date_fin": {"$regex": regex_pattern}}]}
            ]
        })

        document_exploration = list(donnees_ex)
        
        donnees_post = db.mission.find({
        "$and": [
            {'idcoordonnateur': info_user['_id']},
            {'Type': 'post'},
            {'$or': [{"_id": {"$regex": regex_pattern}}, {"Nom": {"$regex": regex_pattern}}, {"Objectif": {"$regex": regex_pattern}}, {"Type": {"$regex": regex_pattern}}, {"Date_deb": {"$regex": regex_pattern}}, {"Date_fin": {"$regex": regex_pattern}}]}
            ]
        })
        document_post = list(donnees_post)
    else:
        if session['type_mission']=="exploration" :
            #missions = db.mission.find({'Type': 'exploration'}) 
            missions = db.mission.find({
            "$and": [
                {'Type': 'exploration'},
                {'$or': [{"_id": {"$regex": regex_pattern}}, {"Nom": {"$regex": regex_pattern}}, {"Objectif": {"$regex": regex_pattern}}, {"Type": {"$regex": regex_pattern}}, {"Date_deb": {"$regex": regex_pattern}}, {"Date_fin": {"$regex": regex_pattern}}]}
                ]
            })
            doc_mission = list(missions)

            for mis in doc_mission:
                id_mission = mis['_id']
                X = db.calendrierMission.count_documents(
                    {'id_mission': id_mission, 'chef_equipe': idU} )

                if X != 0:
                    document_exploration.append(mis)
        
        if session['type_mission']=="post" :            
            #missions = db.mission.find({'Type': 'post'}) 
            missions = db.mission.find({
            "$and": [
                {'Type': 'post'},
                {'$or': [{"_id": {"$regex": regex_pattern}}, {"Nom": {"$regex": regex_pattern}}, {"Objectif": {"$regex": regex_pattern}}, {"Type": {"$regex": regex_pattern}}, {"Date_deb": {"$regex": regex_pattern}}, {"Date_fin": {"$regex": regex_pattern}}]}
                ]
            })
            doc_mission = list(missions)

            for mis in doc_mission:
                id_mission = mis['_id']
                X = db.calendrierMission.count_documents(
                    {'id_mission': id_mission, 'chef_equipe': idU})

                if X != 0:
                    document_post.append(mis)


        # Passer les documents récupérés à la fonction render_template() de Flask
    if verifierSession() == "Coordonnateur" and session['type_mission']=="exploration" :
        return render_template("consulter_missions.html", poste="Coordonnateur", list_missions=document_exploration , Type_mission=session['type_mission'])
    if verifierSession() == "Coordonnateur" and session['type_mission']=="post":
        return render_template("consulter_missions.html", poste="Coordonnateur", list_missions=document_post , Type_mission=session['type_mission'])
    
    if verifierSession() == "Responsable de matériel" and session['type_mission']=="exploration" :
        return render_template("consulter_missions.html", poste="Responsable de matériel", list_missions=document_exploration , Type_mission=session['type_mission'])
    if verifierSession() == "Responsable de matériel" and session['type_mission']=="post":
        return render_template("consulter_missions.html", poste="Responsable de matériel", list_missions=document_post , Type_mission=session['type_mission'])
    
    if verifierSession() == "chef" and session['type_mission']=="exploration":
        return render_template("consulter_missions.html", role="chef", list_missions=document_exploration , Type_mission=session['type_mission'])
    if verifierSession() == "chef" and session['type_mission']=="post":
        return render_template("consulter_missions.html", role="chef", list_missions=document_post , Type_mission=session['type_mission'])
    
    if verifierSession() == "Personnel médical Chef" and session['type_mission']=="exploration":
        return render_template("consulter_missions.html", poste="Personnel médical Chef", list_missions=document_exploration , Type_mission=session['type_mission'])
    if verifierSession() == "Personnel médical Chef" and session['type_mission']=="post":
        return render_template("consulter_missions.html", poste="Personnel médical Chef", list_missions=document_post , Type_mission=session['type_mission'])

    
   