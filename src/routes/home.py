from flask import render_template,send_file
from src.app import app

# Call the home of the app web
@app.route("/")
def home_present():
    return render_template('home.html')

@app.route("/style.css")
def style_present():
    return send_file('templates/style.css')

@app.route("/proceso_diagrama")
def get_image_proceso():
    return send_file('templates/proceso.png', mimetype='image/png')

@app.route("/datos_graph")
def get_image_estaciones():
    return send_file('templates/mapa_estaciones.png', mimetype='image/png')


@app.route("/cluster_graph")
def get_image_cluster():
    return send_file('templates/mapa_estaciones_lec.png', mimetype='image/png')

