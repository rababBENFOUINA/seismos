from application import app
from flask import Flask,Blueprint, render_template, request,session,redirect, url_for
from pymongo import MongoClient
from application import db
from werkzeug.security import check_password_hash

from application.routes.acceuil import verifierSession

@app.route('/auth/<mission>')
def Relogin(mission):
    session['type_mission'] = mission
    return render_template('authentification.html')
  

        
# Route pour l'authentification de l'utilisateur
@app.route('/auth', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
       
        email = request.form.get('Email')
        password = request.form.get('Password')

        
        user = db.utilisateur.find_one({"email": email})

        
        if user and check_password_hash(user['password'], password):
            
            session['utilisateur_id'] = str(user['_id'])

            if user['mdb_changer'] == 1 :
                return redirect(url_for('acceuil'))
            else :
                return render_template('changer_mdp.html', mdb_changer=user['mdb_changer'] )
                
        else:
            
            error = 'Login ou mot de passe incorrect.'
            return render_template('authentification.html', error=error)
    else:
        
        return render_template('authentification.html')


   


@app.route('/logout')
def logout():
    # Supprimez la session de l'utilisateur
    session.pop('utilisateur_id', None)
    session.pop('type_mission',None)

    return render_template('acceuil_index.html')


 
       
