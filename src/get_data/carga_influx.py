from src.get_data.lee_ree import consulta_ree_hour
from src.get_data.analisis_ree import widget_caract 
from dotenv import load_dotenv
import datetime as dt
import sys
sys.path.insert(1, '../')
from src.connect_db import client_influx

def main():
    # funcion para leer de REE de la API que no necesita KEY esta función pide 
    # el intervalo de importación y luego llama a la lectura por horas de 
    # lee_ree y escribe en la base de datos influx

    diff=dt.timedelta(days=15)
    data_ini=dt.datetime(*pregunta_fecha("begins"),0,0)
    data_fin=dt.datetime(*pregunta_fecha("ends"),0,0)
    while data_fin>data_ini:
        data_fin_sample=data_ini+diff
        if data_fin_sample>data_fin:
            data_fin_sample=data_fin

        print('*** probando a consultar de REE de ',data_ini, " a ", data_fin_sample )
        data=consulta_ree_hour('demanda','demanda-tiempo-real',data_ini,data_fin_sample)
        if data==False:
            print('Error consultando datos')
            return False
        print('*** probando a escribir de ',data_ini, " a ", data_fin_sample )
        escribe_influx('demanda-real',data[0]['attributes']['values'])
        escribe_influx('demanda-programada',data[1]['attributes']['values'])
        escribe_influx('demanda-prevista',data[2]['attributes']['values'])

        data_ini=data_fin_sample

    print('*** termina escritura en db_influx de la demanda-tiempo-real ***')
    client_influx.close()

def escribe_influx(table,values):
    # write in influx the data, table is string with the name of
    # the data, values are a dictionary wtih datetime, value an 
    # percentage 

    dbs=client_influx.get_list_database()
    dbs_list=[]
    if not isinstance(dbs,list):
        for key, value in dbs.iteritems():
            dbs_list.append([value])

    if 'db_ereal' not in dbs_list:
        client_influx.create_database('db_ereal')

    client_influx.switch_database('db_ereal')

    for value in values:
        json_body=[{
            "measurement":table,
            "time":value['datetime'],
            "fields":{
                "value":value['value'],
                "percentage":value['percentage']
                }
            }
            ]
        client_influx.write_points(json_body)

def pregunta_fecha(pregunta):
    check=False
    while check==False:
        var=input(" InfluxDB process - Please introduce the date when the importation " + pregunta + " [YYYY/MM/DD] (i.e 2020/10/01):").split("/")
        try:
            var=[int(e) for e in var]
        except ValueError:
            "Please introduce a valid date"

        if sum([isinstance(e,int) for e in var])==3:
            if var[0]>2019 and var[0]<=dt.datetime.now().year:
                try:
                    dt.datetime(year=var[0],month=var[1],day=var[2])
                    check=True
                except ValueError:
                    "Please introduce a valid date"
                    pass
    return var






if __name__=="__main__":
    main()
