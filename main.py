# Programa para gestionar la bd de energia en tiempo real

import argparse
import sys
import src.config
from src.get_data import carga_influx as c_ix

def main():
    file1 = open("src/main_description.txt","r")
    description_text = '\n'.join( file1.readlines() )
    file1.close()
    parser = argparse.ArgumentParser(description=description_text)

    # optional arguments for initialize the analysis
    parser.add_argument('--get_data_ree', action='store_true',
                help='''Read data from public api REE
                (https://apidatos.ree.es), used for initializated the db''')

    args = parser.parse_args()

    # initialized the db 
    if args.get_data_ree:
        c_ix.main()



if __name__=="__main__":
    main()

