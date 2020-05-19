# Programa para gestionar la bd de energia en tiempo real

import argparse
import sys
import src.config
from src.get_data import carga_influx as c_ix
from src.get_data import carga_esios as c_esios
from src.get_data import carga_aemet as c_aemet
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

    # optional for reading REE API Esios
    parser.add_argument('--get_data_esios', action='store_true',
                help='''Read the data from API ESIOS - REE, which is the platform
                that contains the principal information of the Spanish
                electricity wholesale market''')

    # optional for reading AEMET API
    parser.add_argument('--get_data_aemet', action='store_true',
                help='''Read the data from API AEMET, which has the information
                of the climate variables in Spain. These are relevant varibales
                for the renewable electricity generation''')

    # optional for make a sumary of the db
    parser.add_argument('--describ_db', action='store_true',
                help='''Describe the content of the influx db''')

    args = parser.parse_args()

    # initialized the db 
    if args.get_data_ree:
        c_ix.main()

    if args.get_data_esios:
        c_esios.c_esios()

    if args.get_data_aemet:
        c_aemet.c_aemet()

    if args.describ_db:
        describ_db.describ_db()

if __name__=="__main__":
    main()

