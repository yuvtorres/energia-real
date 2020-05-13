# archivo para leer de Red Eléctrica
import requests
import json
import datetime as dt

def leeree():
    current=dt.datetime.now()

    url="https://apidatos.ree.es/es/datos/"
    datos="balance/balance-electrico"
    query="?start_date="+str(current.year)+"-"+str(current.month).zfill(2)
    query+="-"+str(current.day-1).zfill(2)+"T"+str(current.hour-1).zfill(2)
    query+=":00&end_date="+str(current.year)+"-"+str(current.month).zfill(2)
    query+="-"+str(current.day).zfill(2)+"T"+str(current.hour-1).zfill(2)+":00&time_trunc=hour"
    print(query)
    r=requests.get(url+datos+query)
    json_d=r.json()
    print(json_d.keys())

    return json_d.values()


