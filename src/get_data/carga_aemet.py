import src.connect_db
import requests
from src.connect_db import client_mongo
from src.connect_db import client_influx
from src.config import AEMET_KEY
import datetime as dt

def c_aemet():
    # Función que llena la base ereal (Influx), se debe configurar los parametros de
    # fechas consulta para todas las estaciones al tiempo al consulta trae
    # datos diarios.

    client_influx.switch_database('db_ereal')
    diff_time=dt.timedelta(days=15)
    data_ini=dt.datetime(2020,5,1,0,0) # <---- parámetro configurable
    data_fin=dt.datetime(2020,5,15,0,0) # <---- parámetro configurable

    while data_fin>data_ini:
        # Hace consultas cada 15 días 
        data_fin_temp=data_ini+diff_time
        url="https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/"
        url+=data_ini.isoformat()+"UTC/fechafin/"+data_fin_temp.isoformat()+"UTC/todasestaciones"
        querystring = {"api_key":AEMET_KEY}
        headers = {
            'cache-control': "no-cache"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)

        if response.json()['estado']!=200:
            # si hay un error en la respuesta
            print('**** error:',response.json())
            return response.json()['descripcion']

        url_consulta=response.json()['datos']
        response = requests.request("GET", url_consulta, headers=headers, params=querystring)
        datos=[]
        vals=['racha','velmedia','sol','indicativo']
        print('*** Query and writing climate information *** ',data_ini )
        for lect in response.json():
            # por cada una de las lecturas obtenidas
            if sum([val in lect.keys() for val in vals])==4:
                # si las lecturas tienen todos los valores
                if 'horaracha' in lect.keys() and lect['horaracha'][:2].isdigit():
                    # si la hora de la racha no esta
                    if float(lect['horaracha'][:2])>24:
                        print('*** horaracha error:',lect)
                        data=lect['fecha']+'T00:00Z'
                    else:
                        data=lect['fecha']+'T'+lect['horaracha']+'Z'
                data=lect['fecha']
                racha=float(lect['racha'].replace(',','.'))
                velmedia=float(lect['velmedia'].replace(',','.'))
                sol=float(lect['sol'].replace(',','.'))
                indicativo=lect['indicativo']
                json_body={
                        "measurement":"Clima",
                        "time":data,
                        "fields":{
                            "racha-"+indicativo:racha,
                            "velmedia-"+indicativo:velmedia,
                            "sol-"+indicativo:sol
                            }
                        }
                try:
                    client_influx.write_points([json_body])
                    # escribe en la base de influx
                except Exception as e:
                    # error en la escritura
                    print(e)
                    print(json_body)
                    return False

        data_ini=data_fin_temp # <--- avanza a los siguientes 15 días


def c_aemet_actual(actualiza_meta=False):
    # Funcion de actualización de las lecturas de clima desde AEMET en Influx
    # últimas 24 horas. 
    # utilizando la consulta "convecional todas" el parametro que recibe es
    # verdadero cuando se quiere actualizar el valor de los metadatos.

    client_influx.switch_database('db_ereal')
    url="https://opendata.aemet.es/opendata/api/observacion/convencional/todas"
    querystring = { "api_key":AEMET_KEY }
    headers = { 'cache-control': "no-cache" }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.json()['estado']!=200:
        print('**** error:',response.json())
        return response.json()['descripcion']

    url_consulta=response.json()['datos']
    url_meta=response.json()['metadatos']
    response = requests.request("GET", url_consulta, headers=headers, params=querystring)

    if actualiza_meta:
        c_aemet_actual_mongo_metadatos(url_meta)
    
    k=0
    variables=['fint','idema','vv','vmax','inso']
    print('actualizando ',len(response.json()),' estaciones')
    for lectura in response.json():
        if sum([var in lectura.keys() for var in variables ])==5:
            data=lectura['fint']
            indicativo=lectura['idema']
            velmedia=lectura['vv']
            racha=lectura['vmax']
            sol=lectura['inso']
            json_body={
                    "measurement":"Clima",
                    "time":data,
                    "fields":{
                        "racha-"+indicativo:racha,
                        "velmedia-"+indicativo:velmedia,
                        "sol-"+indicativo:sol
                        }
                    }
            try:
                client_influx.write_points([json_body])
                k+=1
            except Exception as e:
                print(e)
                print(json_body)
                return False

    print('se escribieron ',k,' lecturas completas')



def c_aemet_actual_mongo_metadatos(url_metadatos):
    # actualiza la collection metadatos en mongodb
    querystring = { "api_key":AEMET_KEY }
    headers = { 'cache-control': "no-cache" }
    response = requests.request("GET", url_metadatos, headers=headers, params=querystring)

    db=client_mongo.ereal_collections
    aemet_metadatos=db.aemet_metadatos
    print(db.list_collection_names())
    result=aemet_metadatos.insert(response.json())
    print('*** actualizando metadatos AEMET en Mongo')
