from application import app
from flask import Flask,Blueprint, render_template, request,session,redirect, url_for
from pymongo import MongoClient
from application import db
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from application.routes.acceuil import verifierSession
from application.routes.creerCompte import verify_password

    
# Route pour l'authentification de l'utilisateur
@app.route('/changerMdp', methods=['GET', 'POST'])
def changerMdB():
    
    if request.method == 'POST':
        
        contraintes = {
            'Password': lambda valeur: len(valeur) > 0,
            'NvPassword': lambda valeur: verify_password(valeur),
            'Conf_Nv_Password': lambda valeur: len(valeur) > 0 
        }
       
        password = request.form.get('Password')
        NvPassword = request.form.get('NvPassword')
        Conf_Nv_Password = request.form.get('Conf_Nv_Password')
        
        messages_erreur = {}
        for nom_champ, contrainte in contraintes.items():
            valeur_champ = request.form.get(nom_champ)
            if not contrainte(valeur_champ):
                messages_erreur[nom_champ] = f"champ invalide"

        
        idU = session['utilisateur_id']
        user = db.utilisateur.find_one({"_id": idU})

        
        if user and check_password_hash(user['password'], password):
            # Hacher le mot de passe avant de le stocker dans la base de données
            hashed_password = generate_password_hash(NvPassword)      
            if NvPassword == Conf_Nv_Password and not messages_erreur:
                update = {'$set': {'password': hashed_password,
                                'ConfiPassword': Conf_Nv_Password,
                                "mdb_changer": 1}}
                db.utilisateur.update_one(user, update)
            return redirect(url_for('acceuil'))
            
        return render_template('changer_mdp.html', messages_erreur=messages_erreur)

    else:
        idU = session['utilisateur_id']
        user = db.utilisateur.find_one({"_id": idU})
      
        if verifierSession() == "Coordonnateur" :
           return render_template("changer_mdp.html" , poste ="Coordonnateur" , Type_mission=session['type_mission'],mdb_changer=user['mdb_changer'])
    
    
        if verifierSession() == "Responsable de matériel" :
            return render_template("changer_mdp.html" , poste ="Responsable de matériel",mdb_changer=user['mdb_changer'])
        
        
        
        if verifierSession() == "Responsable d'etat" :
            return render_template("changer_mdp.html" , poste ="Responsable d'etat",mdb_changer=user['mdb_changer'])
        

                    
        if verifierSession() == "Personnel médical Chef" and session['type_mission'] == "post":
                    return render_template("changer_mdp.html" , poste ="Personnel médical Chef",mdb_changer=user['mdb_changer']) 
                
        if verifierSession() == "Personnel médical Membre" and session['type_mission'] == "post":
                    return render_template("changer_mdp.html" , poste ="Personnel médical Membre",mdb_changer=user['mdb_changer'])  
            
 
                    
        if verifierSession() == "Responsable de sécurité Chef" and session['type_mission'] == "post":
                    return render_template("changer_mdp.html" , poste ="Responsable de sécurité Chef",mdb_changer=user['mdb_changer']) 
                
        if verifierSession() == "Responsable de sécurité Membre" and session['type_mission'] == "post":
                    return render_template("changer_mdp.html" , poste ="Responsable de sécurité Membre",mdb_changer=user['mdb_changer'])     
            
            
                
        if verifierSession() == "chef" :
            return render_template("changer_mdp.html" , role ="chef",mdb_changer=user['mdb_changer'])
        
        if verifierSession() == "Sismologue" :
            return render_template("changer_mdp.html" ,poste = "Sismologue",Type_mission=session['type_mission'],mdb_changer=user['mdb_changer'])
        
        
            
            return render_template('changer_mdp.html',)





 
       
