# Programa para gestionar la bd de energia en tiempo real

# Modules from python
import argparse
import sys

# Modules ad-hoc from e-real
import src.config
from src.model import pronostico
from src.model  import cluster
from src.get_data import tool_esios as t_esios
from src.get_data import analisis_ree as a_ree
from src.get_data import carga_influx as c_ix
from src.get_data import carga_esios as c_esios
from src.get_data import carga_aemet as c_aemet
from src.get_data import carga_aemet_actual2 as c_aemet2
from src.get_data import carga_aemet_base as c_aemet_base
from src.get_data import describ_db

def main():
    # Getting the description thats it's showed when the option --help is called
    file1 = open("src/main_description.txt","r")
    description_text = '\n'.join( file1.readlines() )
    file1.close()
    parser = argparse.ArgumentParser(description=description_text)

    # read demand data from REE public API
    parser.add_argument('--get_demand_data_ree', action='store_true',
                help='''Read demand data from public api REE (https://apidatos.ree.es), 
                        asking for import period''')

    # Read all parameters from REE API with privat key and write them in mongoDB on 
    # the collection indicadores_ree
    parser.add_argument('--get_indicators_ree', action='store_true',
                help='''Read indicators from system ESIOS of REE (https://www.esios.ree.es/es) 
                and write them in Mongodb''')

    # optional for reading REE API Esios
    parser.add_argument('--get_data_esios', action='store_true',
                help='''Read the data from API ESIOS - REE, which is the platform
                that contains the main information of the Spanish
                electricity wholesale market, this function is called periodically''')

    # optional for reading AEMET API
    parser.add_argument('--get_data_aemet', action='store_true',
                help='''Read the data from API AEMET, which has the information
                of the climate variables in Spain. These are relevant varibales
                for the renewable electricity generation in the short term''')

    # option for reading AEMET API to charge the stations 
    parser.add_argument('--get_data_stations_aemet', action='store_true',
                help='''Read the data of the metereological stations from API AEMET                        , and charge it in the mongo db: ereal_collections''')

    # optional for reading AEMET API all stations at a time
    parser.add_argument('--get_actual_aemet', action='store_true',
                help='''Read the last 24 hours data from API AEMET, which has the information
                of the climate variables in Spain. These are relevant variables
                for the renewable electricity generation in the short term''')

    # optional for reading AEMET API by station
    parser.add_argument('--get_current_aemet', action='store_true',
                help='''Similar to --get_actual_aemet but it makes the query to 
                a different endpoint in API AEMET ( by weather station )''')

    # optional for make a summary of the db
    parser.add_argument('--describ_db', action='store_true',
                help='''Summary of the content of the influx db''')

    # argument to create clusers 
    parser.add_argument('--create_cluster', action='store_true',
                help='''Create the cluster of weather stations by LatLong''')

    # argument to create clusers 
    parser.add_argument('--make_winds', action='store_true',
                help='''Create the wind forecast by cluster using VAR models''')

    # argument to create clusers 
    parser.add_argument('--make_gen_eo', action='store_true',
                help='''Create the eolic generation forecast using forward NN
                model''')

    args = parser.parse_args()

    # Try to read demadn data from open API of REE and write in InfluxDB 
    if args.get_demand_data_ree:
        c_ix.main()

    # Get the indicators of the data in the open API of REE
    if args.get_indicators_ree:
        t_esios.carga_indicadores()

    # Get data of renewable generation from Esios, it is called periodically 
    if args.get_data_esios:
        t_esios.lee_esios_carga_influx(551) # <- lee eolica generada en tiempo real
        t_esios.lee_esios_carga_influx(1295) # <- lee solar generada en tiempo real

    # Get data from AEMET in a period of time defined by user, the data are daily 
    if args.get_data_aemet:
        c_aemet.c_aemet()

    # Get list of the weather stations with some metadata and write it in MongoDB collection
    if args.get_data_stations_aemet:
        c_aemet_base.c_aemet_estaciones()

    # Get data of the last 24 hours from AEMET, if it is necessary to update
    # the metadatos of mongo set true as argument 
    if args.get_actual_aemet:
        c_aemet.c_aemet_actual()

    # Similar to get_actual_aemet, but it makes the query to other endpoint in AEMET% by weather station and shows all the process 
    if args.get_current_aemet:
        c_aemet2.c_aemet_por_estaciones()

    # Show a summary of the data in dbs
    if args.describ_db:
        describ_db.describ_db()

    if args.create_cluster:
        cluster.crea_cluster()

    if args.make_winds:
        cluster.make_winds()

    if args.make_gen_eo:
        pronostico.make_gen_eo()

if __name__=="__main__":
    main()

