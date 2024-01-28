from application import app
from flask import Flask,Blueprint, redirect, render_template, request ,flash, session, url_for
from pymongo import MongoClient
from application import db
from werkzeug.security import generate_password_hash
import re

from application.routes.acceuil import verifierSession

def verify_password(password):
    # Vérifie la longueur minimale du mot de passe
    if len(password) < 8:
        return False

    # Vérifie si le mot de passe contient des lettres majuscules et minuscules, des chiffres et des symboles
    if not re.search(r'[a-z]', password) or not re.search(r'[A-Z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[^a-zA-Z0-9]', password):
        return False

    # Vérifie si le mot de passe contient des mots courants
    common_passwords = ['password', '123456', 'qwerty']
    if password.lower() in common_passwords:
        return False

    return True



@app.route("/CreerCompte")
def formulair_creer_Compte():
    messages_erreur = {}
    if verifierSession() == "Coordonnateur" :
        return render_template("creerCompte.html" , poste ="Coordonnateur" , messages_erreur=messages_erreur , Type_mission=session['type_mission'])
    if verifierSession() == "Responsable de matériel" :
        return render_template("creerCompte.html" , poste ="Responsable de matériel" , messages_erreur=messages_erreur)
    if verifierSession() == "chef" :
        return render_template("creerCompte.html" , role = "chef" , messages_erreur=messages_erreur)
    if verifierSession() == "Personnel médical Chef" :
        return render_template("creerCompte.html" , role = "Personnel médical Chef" , messages_erreur=messages_erreur)


# Route pour creeation des comptes d'utilisateurs
@app.route('/CreerCompte', methods=['GET','POST']) 
def inscrire():
    if request.method == 'POST':
        
        contraintes = {
            'Nom': lambda valeur: len(valeur) > 0 and len(valeur) <= 50 and bool(re.match('^[a-zA-ZÀ-ÿ-0-9 ]+$', valeur)),
            'Prenom': lambda valeur: len(valeur) > 0 and len(valeur) <= 500 and bool(re.match('^[a-zA-ZÀ-ÿ-0-9 ]+$', valeur)),
            'email': lambda valeur: len(valeur) > 0 and len(valeur) <= 255 and bool(re.match('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$', valeur)),
            'Password': lambda valeur: verify_password(valeur),
            'ConfiPassword': lambda valeur: len(valeur) > 0 ,
            'poste': lambda valeur: len(valeur) > 0 
        }
        # Récupération des données de l'utilisateur à partir du formulaire HTML
        nom = request.form.get('Nom')
        Prenom = request.form.get('Prenom')
        email = request.form.get('email')
        password = request.form.get('Password')
        ConfiPassword = request.form.get('ConfiPassword')
        poste = request.form.get('poste')
        
        if verifierSession() == "Coordonnateur"  :
            role = "Chef d'équipe" 
        else : 
            role = "Membre"    
        
        messages_erreur = {}
    for nom_champ, contrainte in contraintes.items():
        valeur_champ = request.form.get(nom_champ)
        if not contrainte(valeur_champ):
            messages_erreur[nom_champ] = f"champ invalide"
        
        utilisateur = session['utilisateur_id']

        # Hacher le mot de passe avant de le stocker dans la base de données
        hashed_password = generate_password_hash(password)
        

    if password == ConfiPassword and not messages_erreur :
        nombre_elements = db.utilisateur.count_documents({})
        idUtilisateur = "U" + str(nombre_elements)
        info_utilisateur = {
                    "_id":idUtilisateur,
                    "Nom": nom,
                    "Prenom": Prenom,
                    "email": email,
                    "password": hashed_password,
                    "ConfiPassword": ConfiPassword,
                    "poste": poste,
                    "role" : role,
                    "idutilisateur":utilisateur,
                    "mdb_changer":0 #champ permet de changer le mot de passe 
                    }
        db.utilisateur.insert_one(info_utilisateur)
        
    if verifierSession() == "Coordonnateur" :
        return render_template("creerCompte.html" , poste ="Coordonnateur" , messages_erreur=messages_erreur , Type_mission=session['type_mission'])
    if verifierSession() == "chef" :
        return render_template("creerCompte.html" , role = "chef" , messages_erreur=messages_erreur)
    if verifierSession() == "Personnel médical Chef" :
        return render_template("creerCompte.html" , role = "Personnel médical Chef" , messages_erreur=messages_erreur)
    if verifierSession() == "admin" :
        return render_template("creerCompte.html" , poste = "admin" , messages_erreur=messages_erreur)
    
    return render_template("creerCompte.html" , poste ="Responsable de matériel" , messages_erreur=messages_erreur)


@app.route('/CreerCompteMembre', methods=['GET','POST']) 
def inscrire_membre():
    if request.method == 'POST':
        
        contraintes = {
            'Nom': lambda valeur: len(valeur) > 0 and len(valeur) <= 50 and bool(re.match('^[a-zA-ZÀ-ÿ-0-9 ]+$', valeur)),
            'Prenom': lambda valeur: len(valeur) > 0 and len(valeur) <= 500 and bool(re.match('^[a-zA-ZÀ-ÿ-0-9 ]+$', valeur)),
            'email': lambda valeur: len(valeur) > 0 and len(valeur) <= 255 and bool(re.match('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$', valeur)),
        }
        # Récupération des données de l'utilisateur à partir du formulaire HTML
        nom = request.form.get('Nom')
        Prenom = request.form.get('Prenom')
        email = request.form.get('email')
        poste = request.form.get('poste')
        role = "Membre"    
        
        messages_erreur = {}
        for nom_champ, contrainte in contraintes.items():
            valeur_champ = request.form.get(nom_champ)
            if not contrainte(valeur_champ):
                messages_erreur[nom_champ] = f"champ invalide"
        
        utilisateur = session['utilisateur_id']

        if not messages_erreur:
            nombre_elements = db.utilisateur.count_documents({})
            idUtilisateur = "U" + str(nombre_elements)
            info_utilisateur = {
                "_id":idUtilisateur,
                "Nom": nom,
                "Prenom": Prenom,
                "email": email,
                "poste": poste,
                "role" : role,
                "idutilisateur":utilisateur
            }
            db.utilisateur.insert_one(info_utilisateur)
        
        return render_template("creerCompte.html" , role = "chef" , messages_erreur=messages_erreur)




@app.route("/Consulter_Info_Compte/<id>")
def Consulter_info_Compte(id):
    users = db.utilisateur.find({"_id":id})
    if verifierSession() == "Coordonnateur" :
        return render_template("consulter_info_compte.html" , poste ="Coordonnateur" , users=users , Type_mission=session['type_mission'])
    if verifierSession() == "chef" :
        return render_template("consulter_info_compte.html" , role = "chef" , users=users)
    if verifierSession() == "Personnel médical Chef" :
        return render_template("consulter_info_compte.html" , role = "Personnel médical Chef" , users=users)
    

@app.route("/ModifierCompte" ,methods=['POST'])
def ModifierCompte():
    if request.method == 'POST':
        id = request.form.get('id')
        
        contraintes = {
            'Nom': lambda valeur: len(valeur) > 0 and len(valeur) <= 50 and bool(re.match('^[a-zA-ZÀ-ÿ-0-9 ]+$', valeur)),
            'Prenom': lambda valeur: len(valeur) > 0 and len(valeur) <= 500 and bool(re.match('^[a-zA-ZÀ-ÿ-0-9 ]+$', valeur)),
            'email': lambda valeur: len(valeur) > 0 and len(valeur) <= 255 and bool(re.match('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$', valeur)),
            'Password': lambda valeur: verify_password(valeur),
            'ConfiPassword': lambda valeur: len(valeur) > 0 
        }
        # Récupération des données de l'utilisateur à partir du formulaire HTML
        nom = request.form.get('Nom')
        Prenom = request.form.get('Prenom')
        email = request.form.get('email')
        password = request.form.get('Password')
        ConfiPassword = request.form.get('ConfiPassword')
        poste = request.form.get('poste')
        
        if verifierSession() == "Coordonnateur" :
            role = "Chef d'équipe"
        else : 
            role = "Membre"    
        
        messages_erreur = {}
    for nom_champ, contrainte in contraintes.items():
        valeur_champ = request.form.get(nom_champ)
        if not contrainte(valeur_champ):
            messages_erreur[nom_champ] = f"champ invalide"

        # Hacher le mot de passe avant de le stocker dans la base de données
        hashed_password = generate_password_hash(password)
       
    utilisateur = session['utilisateur_id']    
    filter = {'_id': id}
    if password == ConfiPassword and not messages_erreur :
        update = { '$set': {
                                        "Nom": nom,
                                        "Prenom": Prenom,
                                        "email": email,
                                        "password": hashed_password,
                                        "ConfiPassword": ConfiPassword,
                                        "poste": poste,
                                        "role" : role,
                                        "idutilisateur":utilisateur
                                        }}
        
        db.utilisateur.update_one(filter, update)
        
        
    if verifierSession() == "Coordonnateur" :
        return redirect(url_for('afficher_equipe', Type_mission=session['type_mission']))


       
