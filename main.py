# Programa para gestionar la bd de energia en tiempo real

# Modules efrom python
import argparse
import sys
import src.config

# Modules ad-hoc from e-real
from src.get_data import tool_esios as t_esios
from src.get_data import analisis_ree as a_ree
from src.get_data import carga_influx as c_ix
from src.get_data import carga_esios as c_esios
from src.get_data import carga_aemet as c_aemet
from src.get_data import carga_aemet_actual2 as c_aemet2
from src.get_data import carga_aemet_base as c_aemet_base
from src.get_data import describ_db

def main():
    file1 = open("src/main_description.txt","r")
    description_text = '\n'.join( file1.readlines() )
    file1.close()
    parser = argparse.ArgumentParser(description=description_text)

    # optional for read REE public API
    parser.add_argument('--get_data_ree', action='store_true',
                help='''Read data from public api REE
                (https://apidatos.ree.es), used for initializated the db''')

    # optional for read REE public API and write in Inlfux db some parameters
    parser.add_argument('--get_data_ree2', action='store_true',
                help='''Read data from public api REE
                (https://apidatos.ree.es), some parameters used for initializated the db''')


    # optional for reading REE API Esios
    parser.add_argument('--get_data_esios', action='store_true',
                help='''Read the data from API ESIOS - REE, which is the platform
                that contains the main information of the Spanish
                electricity wholesale market''')

    # optional for reading AEMET API
    parser.add_argument('--get_data_aemet', action='store_true',
                help='''Read the data from API AEMET, which has the information
                of the climate variables in Spain. These are relevant varibales
                for the renewable electricity generation in the short term''')

    # option for reading AEMET API to charge the stations 
    parser.add_argument('--get_data_aemet_base', action='store_true',
                help='''Read the data of the metereological stations from API AEMET,
                and charge it in the mongo db: ereal_collections.''')

    # optional for reading AEMET API all stations at a time
    parser.add_argument('--get_actual_aemet', action='store_true',
                help='''Read the last 24 hours data from API AEMET, which has the information
                of the climate variables in Spain. These are relevant variables
                for the renewable electricity generation in the short term''')

    # optional for reading AEMET API by station
    parser.add_argument('--get_actual_aemet2', action='store_true',
                help='''Read the last 24 hours data from API AEMET by stations''')

    # optional for make a sumary of the db
    parser.add_argument('--describ_db', action='store_true',
                help='''Describe the content of the influx db''')

    args = parser.parse_args()

    # initialized the db 
    if args.get_data_ree:
        c_ix.main()

    if args.get_data_ree2:
        t_esios.carga_indicadores()
#        a_ree.widget_caract()

    if args.get_data_esios:
#        c_esios.c_esios()
        t_esios.lee_esios_carga_influx(551) # <- lee eolica generada en timpo real
        t_esios.lee_esios_carga_influx(552) # <- lee solar generada en timpo real


    if args.get_data_aemet:
        c_aemet.c_aemet()

    if args.get_data_aemet_base:
        c_aemet_base.c_aemet_estaciones()

    if args.get_actual_aemet:
        # set true as argument to update the metadatos of mongodb
        c_aemet.c_aemet_actual()

    if args.get_actual_aemet2:
        # set true as argument to update the metadatos of mongodb
        c_aemet2.c_aemet_por_estaciones()

    if args.describ_db:
        describ_db.describ_db()

if __name__=="__main__":
    main()

