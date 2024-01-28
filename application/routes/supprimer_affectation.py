from application import app
from flask import Flask,Blueprint, redirect, url_for
from application import db
import folium

from application.routes.acceuil import verifierSession


@app.route('/supp_affectation/<id>')
def supp_affectation(id):
    result = db.affectation.delete_one({"_id": id})
    return redirect(url_for('gerer_membre')) 
