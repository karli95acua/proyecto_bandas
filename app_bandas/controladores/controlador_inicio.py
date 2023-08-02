from app_bandas import app
from flask import render_template

@app.route('/inicio', methods=['GET'])
def desplegar_inicio():
    return render_template("inicio.html")
