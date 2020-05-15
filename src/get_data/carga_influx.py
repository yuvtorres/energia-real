from src.get_data.lee_ree import consulta_ree_hour
from src.get_data.analisis_ree import leeree
from dotenv import load_dotenv
import datetime as dt
import sys
sys.path.insert(1, '../')
from src.connect_db import client_influx

def main():
    
    diff=dt.timedelta(days=15)
    data_ini=dt.datetime(2019,2,1,0,0)
    data_fin=dt.datetime(2020,1,1,0,0)
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


if __name__=="__main__":
    main()
