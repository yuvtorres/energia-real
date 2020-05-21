from flask import render_template,send_file
from src.app import app

# Call the home of the app web
@app.route("/")
def home_present():
    return render_template('home.html')

@app.route("/m_estaciones")
def get_image_route():
    return send_file('templates/mapa_estaciones.png', mimetype='image/png')


@app.route("/m_estaciones_lec")
def get_image_all_sentiments():
    return send_file('templates/mapa_estaciones_lec.png', mimetype='image/png')

