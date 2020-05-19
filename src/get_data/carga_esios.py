import src.connect_db
import requests
from src.connect_db import client_influx
from src.config import REE_KEY
import datetime as dt

def c_esios():
    diff_time=dt.timedelta(days=15)
    data_ini=dt.datetime(2020,1,1,0,0)
    data_fin=dt.datetime(2020,5,15,0,0)
    url='https://api.esios.ree.es/indicators/'
    indicator=['10206']
    header={'Accept': 'application/json;application/vnd.esios-api-v1+json',
            'Content-Type': 'application/json',
            'Host': 'api.esios.ree.es',
            'Authorization': f'Token token={REE_KEY}'}
    while data_fin > data_ini:
        data_fin_diff=data_ini+diff_time
        if data_fin_diff>data_fin:
            data_fin_diff=data_fin
        parm={'start_date':data_ini,
              'end_date':data_fin_diff}
        res=requests.get(url+indicator[0],params=parm,headers=header)
        name=res.json()['indicator']['name']
        values=res.json()['indicator']['values']
        print('writing in influx...',data_ini )
        escribe_influx(name, values)
        data_ini=data_fin_diff

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

