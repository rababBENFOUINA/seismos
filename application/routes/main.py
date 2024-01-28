from application import app
from flask import Flask,Blueprint, render_template


@app.route("/")
def index():
    return render_template("acceuil_index.html")