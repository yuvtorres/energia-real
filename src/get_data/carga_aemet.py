import src.connect_db
import requests
from src.connect_db import client_influx
from src.config import AEMET_KEY
import datetime as dt

def c_aemet():
    client_influx.switch_database('db_ereal')
    diff_time=dt.timedelta(days=15)
    data_ini=dt.datetime(2020,1,1,0,0)
    data_fin=dt.datetime(2020,5,15,0,0)

    while data_fin>data_ini:
        data_fin_temp=data_ini+diff_time
        url="https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/"
        url+=data_ini.isoformat()+"UTC/fechafin/"+data_fin_temp.isoformat()+"UTC/todasestaciones"

        querystring = {"api_key":AEMET_KEY}
        headers = {
            'cache-control': "no-cache"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.json()['estado']!=200:
            print('**** error:',response.json())
            return response.json()['descripcion']

        url_consulta=response.json()['datos']
        response = requests.request("GET", url_consulta, headers=headers, params=querystring)
        datos=[]
        print('*** Query and writing climate information *** ',data_ini )
        for lect in response.json():
            if 'horaracha' in lect.keys() and lect['horaracha'][:2].isdigit():
                if float(lect['horaracha'][:2])>24:
                    print('*** horaracha error:',lect)
                    data=lect['fecha']
                else:
                    data=lect['fecha']+'T'+lect['horaracha']
            else:
                data=lect['fecha']
            if 'racha' in lect.keys():
                racha=float(lect['racha'].replace(',','.'))
            else:
                racha=-1
            if 'velmedia' in lect.keys():
                velmedia=float(lect['velmedia'].replace(',','.'))
            else:
                velmedia=-1
            if 'sol' in lect.keys(): 
                sol=float(lect['sol'].replace(',','.'))
            else:
                sol=-1
            indicativo=lect['indicativo']
            json_body={
                    "measurement":"Clima",
                    "time":data,
                    "fields":{
                        "racha":racha,
                        "velmedia":velmedia,
                        "sol":sol,
                        "indicativo":indicativo
                        }
                    }
            datos.append(json_body)
            client_influx.write_points(datos)
            data_ini=data_fin_temp










