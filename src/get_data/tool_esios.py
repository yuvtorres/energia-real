# Archivo que contiene la función que lee los indicadores de REE Esios y
# escribe en mongo DB los mismo para su gestión.
import src.connect_db
import requests
from src.connect_db import client_mongo
from src.config import REE_KEY
import datetime as dt

def carga_indicadores():
    url='https://api.esios.ree.es/indicators'
    header={'Accept': 'application/json;application/vnd.esios-api-v1+json',
            'Content-Type': 'application/json',
            'Host': 'api.esios.ree.es',
            'Authorization': f'Token token="{REE_KEY}"'}
    res=requests.get(url,headers=header)

    datos=res.json()
    db=client_mongo.ereal_collections
    print()
    print('*** Fueron cargados ',len(datos['indicators']) , ' indicadores en mongo DB ')
    db.indicadores_ree.insert_many(datos['indicators'])
    
def lee_esios_carga_influx(id=551):
    # funcion para la lectura en tiempo real de la generación eólica (id=551) últimas
    # tres horas D-1 hasta la hora actual
    url='https://api.esios.ree.es/indicators/'
    indicator=[id]
    data_ini=
    data_fin=
    header={'Accept': 'application/json;application/vnd.esios-api-v1+json',
            'Content-Type': 'application/json',
            'Host': 'api.esios.ree.es',
            'Authorization': f'Token token={REE_KEY}'}
    
    parm={'start_date':data_ini,
            'end_date':data_fin}

    res=requests.get(url+indicator[0],params=parm,headers=header)
    name=res.json()['indicator']['name']
    values=res.json()['indicator']['values']
    print('writing in influx...',data_ini )
    escribe_influx(name, values)


def escribe_influx(name, values):
    dbs=client_influx.get_list_database()
    dbs_list=[]
    if not isinstance(dbs,list):
        for key, value in dbs.iteritems():
            dbs_list.append(value)

    if 'db_ereal' not in dbs_list:
        client_influx.create_database('db_ereal')

    client_influx.switch_database('db_ereal')

    for value in values:
        json_body=[{
            "measurement":name,
            "time":value["datetime"],
            "fields":{
                "value":value["value"],
                "geo_id": value["geo_id"]
                }
            }]
        client_influx.write_points(json_body)

