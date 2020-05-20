import src.connect_db
import requests
from src.connect_db import client_mongo
from src.connect_db import client_influx
from src.config import AEMET_KEY
import datetime as dt

def c_aemet_estaciones():
    # funcion para cargar las estaciones en mongodb
    url="https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"
    querystring = { "api_key":AEMET_KEY }
    headers = { 'cache-control': "no-cache" }
    response = requests.request("GET", url, headers=headers, params=querystring)
    db=client_mongo.ereal_collections
    url_datos=response.json()['datos']
    c_aemet_actualiza_metadatos_estaciones(response.json()['metadatos'])
    response = requests.request("GET", url_datos,headers=headers, params=querystring)
    print('-> actualizando',len(response.json()) ,' estaciones' )
    db=client_mongo.ereal_collections
    aemet_estaciones=db.aemet_estaciones
    result=aemet_estaciones.insert_many(response.json())


def c_aemet_actualiza_metadatos_estaciones(url_metadatos):
    # actualiza la collection metadatos en mongodb
    querystring = { "api_key":AEMET_KEY }
    headers = { 'cache-control': "no-cache" }
    response = requests.request("GET", url_metadatos, headers=headers, params=querystring)

    db=client_mongo.ereal_collections
    aemet_metadatos_estaciones=db.aemet_metadatos_estaciones
    result=aemet_metadatos_estaciones.insert(response.json())
    print('*** actualizando metadatos de estaciones de AEMET en Mongo')

def c_aemet_actualiza_municipios():
    url = "https://opendata.aemet.es/opendata/api/maestro/municipios"
    querystring = {"api_key":AEMET_KEY}
    headers = {
            'cache-control': "no-cache"
            }
    response = requests.request("GET", url, headers=headers, params=querystring)
    db=client_mongo.ereal_collections
    municipio=db.municipio
    result=municipio.insert_many(response.json())

