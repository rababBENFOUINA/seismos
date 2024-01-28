from pymongo import MongoClient
from application import db
from application import app
from flask import Flask,Blueprint, render_template, request, session


@app.route("/acceuil")
def acceuil():
    if verifierSession() == "Coordonnateur" :
        return render_template("acceuil.html" , poste ="Coordonnateur" , Type_mission=session['type_mission'])
    
    
    
    if verifierSession() == "Responsable de matériel" :
        return render_template("acceuil.html" , poste ="Responsable de matériel")
    
    
    
    if verifierSession() == "Responsable d'etat" :
        return render_template("acceuil.html" , poste ="Responsable d'etat")

    if verifierSession() == "admin" :
        messages_erreur=[]
        return render_template("creerCompte.html" , poste ="admin",messages_erreur=messages_erreur)
    
    
    
    if verifierSession() == "Personnel médical Chef" and session['type_mission'] == "exploration":
                error = 'Vous n\'avez pas le droit de vous connecter à cette partie de l\'application.'
                return render_template('authentification.html', error=error)
            
    if verifierSession() == "Personnel médical Membre" and session['type_mission'] == "exploration":
                error = 'Vous n\'avez pas le droit de vous connecter à cette partie de l\'application.'
                return render_template('authentification.html', error=error) 
                   
    if verifierSession() == "Personnel médical Chef" and session['type_mission'] == "post":
                return render_template("acceuil.html" , poste ="Personnel médical Chef") 
            
    if verifierSession() == "Personnel médical Membre" and session['type_mission'] == "post":
                return render_template("acceuil.html" , poste ="Personnel médical Membre")  
        
        
        
    if verifierSession() == "Responsable de sécurité Chef" and session['type_mission'] == "exploration":
                error = 'Vous n\'avez pas le droit de vous connecter à cette partie de l\'application.'
                return render_template('authentification.html', error=error)
            
    if verifierSession() == "Responsable de sécurité Membre" and session['type_mission'] == "exploration":
                error = 'Vous n\'avez pas le droit de vous connecter à cette partie de l\'application.'
                return render_template('authentification.html', error=error) 
                   
    if verifierSession() == "Responsable de sécurité Chef" and session['type_mission'] == "post":
                return render_template("acceuil.html" , poste ="Responsable de sécurité Chef") 
            
    if verifierSession() == "Responsable de sécurité Membre" and session['type_mission'] == "post":
                return render_template("acceuil.html" , poste ="Responsable de sécurité Membre")     
        
         
            
    if verifierSession() == "chef" :
        return render_template("acceuil.html" , role ="chef")
    
    if verifierSession() == "Sismologue" :
        return render_template("acceuil.html" , poste ="Sismologue",Type_mission=session['type_mission'])
    
          



    
def verifierSession():
    user=session['utilisateur_id']
    poste = db.utilisateur.find({ '_id' : user})
    
    documents = list(poste)
    if documents:
        document = documents[0]
        if document['poste'] == "Coordonnateur" :
                return "Coordonnateur" 
        
        if document['poste'] == "Responsable de matériel" :
                return "Responsable de matériel"  
        
        if document['poste'] == "Responsable d'etat" :
                return "Responsable d'etat"  
        
        if( document['poste'] == "Personnel médical") and (document['role'] =="Chef d'équipe") :
                return "Personnel médical Chef" 
        if (document['poste'] == "Personnel médical") and (document['role'] =="Membre") :
                return "Personnel médical Membre"  
           
        if( document['poste'] == "Responsable de sécurité") and (document['role'] =="Chef d'équipe") :
                return "Personnel médical Chef" 
        if (document['poste'] == "Responsable de sécurité") and (document['role'] =="Membre") :
                return "Responsable de sécurité Membre"  
                  
        if document['role'] =="Chef d'équipe" and not (document['poste'] == "Responsable de matériel") :
                return "chef"
        if document['poste'] == "Sismologue" :
                return "Sismologue"
        if document['poste'] == "admin" :
                return "admin"
          
            
    