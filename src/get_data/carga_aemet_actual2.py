import requests
import datetime as dt
import time
import src.connect_db
from src.connect_db import client_mongo
from src.connect_db import client_influx
from src.config import AEMET_KEY

def c_aemet_por_estaciones():
    # funcion para cargar por estaciones los datos en influxdb
    # la consulta devuelve datos para las últimas 24 horas
    client_influx.switch_database('db_ereal')
    url="https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/"
    querystring = { "api_key":AEMET_KEY }
    headers = { 'cache-control': "no-cache" }

    k=0
    k_t=0
    escribe=False
    db=client_mongo.ereal_collections
    estaciones=list(db.estaciones.find({},{'_id':0,'indicativo':1}))
    for estacion in estaciones:
        response = requests.request("GET", url+estacion['indicativo'],
                headers=headers, params=querystring)

        if (response.json()['estado'])==200:
            url_datos=response.json()['datos']
            response = requests.request("GET", url_datos,headers=headers,params=querystring)
            try:
                response=response.json()
            except:
                print(response)
                response=[]
                estaciones.append(estacion)
        elif (response.json()['estado'])==429:
            print('Esperando al próximo minuto...')
            time.sleep(60)
            estaciones.append(estacion)
            response=[]
        else:
            print('error leyedo la estacion',estacion['indicativo'],'descripcion:'
                    ,response.json()['descripcion'])
            response=[]

        for lectura in response:
            k_t=+1
            if sum([var in lectura.keys() for var in ['vv','inso']])==2:
                escribe=True
                k=+1
                data=lectura['fint']
                velmedia=lectura['vv']
                inso=lectura['inso']
            elif sum([var in lectura.keys() for var in ['vvu','inso']])==2:
                escribe=True
                k=+1
                data=lectura['fint']
                velmedia=lectura['vv']
                inso=lectura['inso']

            if escribe:
                escribe=False

                json_body={
                        "measurement":"Clima",
                        "time":data,
                        "fields":{
                            "velmedia-"+estacion['indicativo']:velmedia,
                            "inso-"+estacion['indicativo']:inso
                            }
                        }
                client_influx.write_points([json_body])


    print('-> total actualizaciones: ',k,' de ',k_t,' posibles')


