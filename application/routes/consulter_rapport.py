import base64
import re
from application import app
from flask import Flask, Blueprint, abort, render_template, request, send_file, session
from application import db
from io import BytesIO

from application.routes.acceuil import verifierSession

@app.route("/Consulter_informations_rapport")
def list_rapports():
    if verifierSession() == "Coordonnateur" :
        return render_template("consulter_rapport.html" , poste ="Coordonnateur")
    if verifierSession() == "Responsable de matériel" :
        return render_template("consulter_rapport.html" , poste ="Responsable de matériel")
    if verifierSession() == "Responsable d'etat" :
        return render_template("consulter_rapport.html" , poste ="Responsable d'etat")
    if verifierSession() == "Personnel médical Chef" :
        return render_template("consulter_rapport.html" , role = "Personnel médical Chef")
    if verifierSession() == "chef" :
        return render_template("consulter_rapport.html" , role = "chef")

@app.route('/afficher_rapport', methods=['GET', 'POST'])
def afficher_rapport():
    document_exploration = []
    document_post = []
    idU = session['utilisateur_id']
    info_user = db.utilisateur.find_one({'_id': idU})

    if info_user and info_user.get('poste') == 'Coordonnateur':
        missions = db.mission.find({'idcoordonnateur': info_user['_id']})
        for mission in missions:
            if mission['Type'] == "exploration":
                rapports = db.rapport.find({'id_mission': mission['_id'], 'Destinataire': 'Coordonnateur'})
                for rapport in rapports:
                    document_exploration.append(rapport)
                    
            if mission['Type'] == "post":
                rapports = db.rapport.find({'id_mission': mission['_id'], 'Destinataire': 'Coordonnateur'})
                for rapport in rapports:
                    document_post.append(rapport)        
    else:
        if session['type_mission']=="exploration" :
            rapports = db.rapport.find({'Destinataire': info_user.get('poste')})
            doc_rapp = list(rapports)
            for rapport in doc_rapp:
                missions = db.mission.find({'Type': "exploration"}) 
                id_mission = rapport['id_mission']
                for mission in missions:
                    if mission['_id'] == id_mission:
                        X = db.calendrierMission.count_documents(
                            {'id_mission': id_mission, 'chef_equipe': idU})
                        if X != 0:
                            document_exploration.append(rapport)
                            
        
        if session['type_mission']=="post" :
            rapports = db.rapport.find({'Destinataire': info_user.get('poste')})
            doc_rapp = list(rapports)
            for rapport in doc_rapp:
                missions = db.mission.find({'Type': "post"}) 
                id_mission = rapport['id_mission']
                for mission in missions:
                    if mission['_id'] == id_mission:
                        X = db.calendrierMission.count_documents(
                            {'id_mission': id_mission, 'chef_equipe': idU})
                        if X != 0:
                            document_post.append(rapport)                    

    # Passer les documents récupérés à la fonction render_template() de Flask
    if verifierSession() == "Coordonnateur" and session['type_mission']=="exploration":
        return render_template("consulter_rapport.html" , poste ="Coordonnateur" , list_rapports=document_exploration , Type_mission=session['type_mission'])
    if verifierSession() == "Responsable de matériel" and session['type_mission']=="exploration":
        return render_template("consulter_rapport.html" , poste ="Responsable de matériel" , list_rapports=document_exploration)
    if verifierSession() == "Responsable d'etat" and session['type_mission']=="exploration":
        return render_template("consulter_rapport.html" , poste ="Responsable d'etat" , list_rapports=document_exploration)
    if verifierSession() == "chef" and session['type_mission']=="exploration":
        return render_template("consulter_rapport.html" , role = "chef" , list_rapports=document_exploration)
    if verifierSession() == "Personnel médical Chef" and session['type_mission']=="exploration":
        return render_template("consulter_rapport.html" , role = "Personnel médical Chef" , list_rapports=document_exploration)
    if verifierSession() == "Sismologue" and session['type_mission']=="exploration":
        return render_template("consulter_rapport.html" , poste = "Sismologue" , list_rapports=document_exploration,Type_mission=session['type_mission'])

    if verifierSession() == "Coordonnateur" and session['type_mission']=="post":
        return render_template("consulter_rapport.html" , poste ="Coordonnateur" , list_rapports=document_post , Type_mission=session['type_mission'])
    if verifierSession() == "Responsable de matériel" and session['type_mission']=="post":
        return render_template("consulter_rapport.html" , poste ="Responsable de matériel" , list_rapports=document_post)
    if verifierSession() == "Responsable d'etat" and session['type_mission']=="post":
        return render_template("consulter_rapport.html" , poste ="Responsable d'etat" , list_rapports=document_post)
    if verifierSession() == "chef" and session['type_mission']=="post":
        return render_template("consulter_rapport.html" , role = "chef" , list_rapports=document_post)
    if verifierSession() == "Personnel médical Chef" and session['type_mission']=="post":
        return render_template("consulter_rapport.html" , role = "Personnel médical Chef" , list_rapports=document_post)
    if verifierSession() == "Sismologue" and session['type_mission']=="post":
        return render_template("consulter_rapport.html" , poste = "Sismologue" , list_rapports=document_post,Type_mission=session['type_mission'])

######################################################################################################################################################
@app.route("/filtrer_liste_rapport")
def filtrer_liste_rapport():
    messages_erreur = {}
    valeur = request.args.get('valeur')
    regex_pattern = re.compile(valeur, re.IGNORECASE)
    
    
    document_exploration = []
    document_post = []
    idU = session['utilisateur_id']
    info_user = db.utilisateur.find_one({'_id': idU})

    if info_user and info_user.get('poste') == 'Coordonnateur':
        missions = db.mission.find({'idcoordonnateur': info_user['_id']})
        for mission in missions:
            if mission['Type'] == "exploration":
               # rapports = db.rapport.find({"$and":{'id_mission': mission['_id']}, {'Destinataire': 'Coordonnateur'},{"$or": [{"_id": {"$regex": valeur}}]}})
                
                rapports = db.rapport.find({
                    "$and": [
                        {'id_mission': mission['_id']},
                        {'Destinataire': 'Coordonnateur'},
                        {"$or": [{"_id": {"$regex": regex_pattern}},{"_id": {"$regex": regex_pattern}},{"titre_rapport": {"$regex": regex_pattern}},{"id_mission": {"$regex": regex_pattern}},{"expediteu": {"$regex": regex_pattern}}]}
                    ]
                })

                for rapport in rapports:
                    document_exploration.append(rapport)
                    
            if mission['Type'] == "post":
                rapports = db.rapport.find({
                    "$and": [
                        {'id_mission': mission['_id']},
                        {'Destinataire': 'Coordonnateur'},
                        {"$or": [{"_id": {"$regex": regex_pattern}},{"_id": {"$regex": regex_pattern}},{"titre_rapport": {"$regex": regex_pattern}},{"id_mission": {"$regex": regex_pattern}},{"expediteu": {"$regex": regex_pattern}}]}
                    ]
                })
                
                for rapport in rapports:
                    document_post.append(rapport)        
    else:
        if session['type_mission']=="exploration" :
            #rapports = db.rapport.find({'Destinataire': info_user.get('poste')})
            rapports = db.rapport.find({
                    "$and": [
                        {'Destinataire': info_user.get('poste')},
                        {"$or": [{"_id": {"$regex": regex_pattern}},{"_id": {"$regex": regex_pattern}},{"titre_rapport": {"$regex": regex_pattern}},{"id_mission": {"$regex": regex_pattern}},{"expediteu": {"$regex": regex_pattern}}]}
                    ]
                })
            
            doc_rapp = list(rapports)
            for rapport in doc_rapp:
                missions = db.mission.find({'Type': "exploration"}) 
                id_mission = rapport['id_mission']
                for mission in missions:
                    if mission['_id'] == id_mission:
                        X = db.calendrierMission.count_documents(
                            {'id_mission': id_mission, 'chef_equipe': idU})
                        if X != 0:
                            document_exploration.append(rapport)
                            
        
        if session['type_mission']=="post" :
            #rapports = db.rapport.find({'Destinataire': info_user.get('poste')})
            rapports = db.rapport.find({
                    "$and": [
                        {'Destinataire': info_user.get('poste')},
                        {"$or": [{"_id": {"$regex": regex_pattern}},{"_id": {"$regex": regex_pattern}},{"titre_rapport": {"$regex": regex_pattern}},{"id_mission": {"$regex": regex_pattern}},{"expediteu": {"$regex": regex_pattern}}]}
                    ]
                })
            doc_rapp = list(rapports)
            for rapport in doc_rapp:
                missions = db.mission.find({'Type': "post"}) 
                id_mission = rapport['id_mission']
                for mission in missions:
                    if mission['_id'] == id_mission:
                        X = db.calendrierMission.count_documents(
                            {'id_mission': id_mission, 'chef_equipe': idU})
                        if X != 0:
                            document_post.append(rapport)                    

    # Passer les documents récupérés à la fonction render_template() de Flask
    if verifierSession() == "Coordonnateur" and session['type_mission']=="exploration":
        return render_template("consulter_rapport.html" , poste ="Coordonnateur" , list_rapports=document_exploration , Type_mission=session['type_mission'])
    if verifierSession() == "Responsable de matériel" and session['type_mission']=="exploration":
        return render_template("consulter_rapport.html" , poste ="Responsable de matériel" , list_rapports=document_exploration, Type_mission=session['type_mission'])
    if verifierSession() == "Responsable d'etat" and session['type_mission']=="exploration":
        return render_template("consulter_rapport.html" , poste ="Responsable d'etat" , list_rapports=document_exploration, Type_mission=session['type_mission'])
    if verifierSession() == "chef" and session['type_mission']=="exploration":
        return render_template("consulter_rapport.html" , role = "chef" , list_rapports=document_exploration, Type_mission=session['type_mission'])
    if verifierSession() == "Personnel médical Chef" and session['type_mission']=="exploration":
        return render_template("consulter_rapport.html" , role = "Personnel médical Chef" , list_rapports=document_exploration, Type_mission=session['type_mission'])
    if verifierSession() == "Sismologue" and session['type_mission']=="exploration":
        return render_template("consulter_rapport.html" , poste = "Sismologue" , list_rapports=document_exploration,Type_mission=session['type_mission'])

    if verifierSession() == "Coordonnateur" and session['type_mission']=="post":
        return render_template("consulter_rapport.html" , poste ="Coordonnateur" , list_rapports=document_post , Type_mission=session['type_mission'])
    if verifierSession() == "Responsable de matériel" and session['type_mission']=="post":
        return render_template("consulter_rapport.html" , poste ="Responsable de matériel" , list_rapports=document_post, Type_mission=session['type_mission'])
    if verifierSession() == "Responsable d'etat" and session['type_mission']=="post":
        return render_template("consulter_rapport.html" , poste ="Responsable d'etat" , list_rapports=document_post, Type_mission=session['type_mission'])
    if verifierSession() == "chef" and session['type_mission']=="post":
        return render_template("consulter_rapport.html" , role = "chef" , list_rapports=document_post, Type_mission=session['type_mission'])
    if verifierSession() == "Personnel médical Chef" and session['type_mission']=="post":
        return render_template("consulter_rapport.html" , role = "Personnel médical Chef" , list_rapports=document_post, Type_mission=session['type_mission'])
    if verifierSession() == "Sismologue" and session['type_mission']=="post":
        return render_template("consulter_rapport.html" , poste = "Sismologue" , list_rapports=document_post,Type_mission=session['type_mission'])

 



#######################################################################################################################################################


@app.route('/telecharger_rapport/<id>')
def telecharger_pdf(id):
    pdf_data = db.rapport.find_one({'_id': id})
    if pdf_data:
        pdf_bytes = base64.b64decode(pdf_data['data'])
        return send_file(BytesIO(pdf_bytes),mimetype='application/pdf',
                     as_attachment=True, download_name=pdf_data['name'])
        

@app.route('/consulter_info_rapport/<id>')        
def consulter_Info_rapport(id):
    rapport=db.rapport.find({'_id':id })
    info_rap=list(rapport)
    if verifierSession() == "Coordonnateur" :
        return render_template("consulter_info_rapport.html" , poste ="Coordonnateur" ,info_rapport=info_rap , Type_mission=session['type_mission'])
    if verifierSession() == "Responsable de matériel" :
        return render_template("consulter_info_rapport.html" , poste ="Responsable de matériel" ,info_rapport=info_rap)
    if verifierSession() == "Responsable d'etat" :
        return render_template("consulter_info_rapport.html" , poste ="Responsable d'etat" ,info_rapport=info_rap)
    if verifierSession() == "chef" :
        return render_template("consulter_info_rapport.html" , role = "chef" ,info_rapport=info_rap)
    if verifierSession() == "Sismologue" :
        return render_template("consulter_info_rapport.html" , role = "Sismologue" ,info_rapport=info_rap, Type_mission=session['type_mission'])

@app.route('/telecharger/<id>')
def telecharger_rapport(id):
    pdf_data = db.rapportEtudeSeisme.find_one({'_id': id})
    if pdf_data:
        pdf_bytes = base64.b64decode(pdf_data['data'])
        if pdf_bytes:
            return send_file(BytesIO(pdf_bytes),
                             as_attachment=True,
                             download_name=pdf_data.get('nom'))
    abort(404)
