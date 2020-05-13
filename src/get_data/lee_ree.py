# archivo para leer de Red Eléctrica
import requests
import json
import datetime as dt

def consulta_ree_hour(end_point, widget, fecha_ini, fecha_fin):
    # Función consultar horaria en REE
    # Apidatos.ree.es
    
    url    = "https://apidatos.ree.es/es/datos/"
    widget = end_point + "/" + widget
    query  = "?start_date=" + str(fecha_ini.year)+"-"+str(fecha_ini.month).zfill(2)
    query += "-"+str(fecha_ini.day).zfill(2)+"T"+str(fecha_ini.hour-1).zfill(2)
    query += ":00&end_date="+str(fecha_fin.year)+"-"+str(fecha_fin.month).zfill(2)
    query += "-"+str(fecha_fin.day).zfill(2)+"T"+str(fecha_fin.hour-1).zfill(2)+":00&time_trunc=hour"

    print("**** consultando -> ",end_point,' - ', widget ," ****")

    header={"Accept":"application/json",
            "Content-Type":"application/json",
            "Host":"apidatos.ree.es"}

    r=requests.get(url+widget+query, headers=header)
    json_d=r.json()
    if 'errors' in json_d.keys():
        return False

    escribe_bd(widget,data)
    return res

