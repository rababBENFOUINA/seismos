from pymongo import MongoClient
from application import db
from application import app
from flask import Flask,Blueprint, jsonify, render_template, request, session

from application.routes.acceuil import verifierSession


@app.route("/Mail")
def mail():
    missions=db.mission.find()
    if verifierSession() == "Responsable d'etat" :
        return render_template("MailAccord.html" , poste ="Responsable d'etat",missions=missions)


@app.route('/get_mail', methods=['GET'])
def get_mail():
    id = request.args.get('id')
    mission = db.mission.find_one({'_id': id}) 
    if mission:
        idutilisateur =mission['idcoordonnateur']
        coordonnateur = db.utilisateur.find_one({'_id':idutilisateur})
        return jsonify({'email': coordonnateur['email']}) # Utiliser les clés 'nom' et 'prenom' pour correspondre aux noms de champ dans le formulaire
    else:
        # Retourner une réponse vide si le membre n'est pas trouvé
        return jsonify({})