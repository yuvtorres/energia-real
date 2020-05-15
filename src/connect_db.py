from influxdb import InfluxDBClient
from influxdb import DataFrameClient
import src.config

#from dotenv import load_dotenv
#from pathlib import Path
import os
#
#last_dir=os.getcwd().split('/')[-1]
#
#if last_dir=='src':
#    env_path = Path('..') / '.env'
#elif last_dir=='get_data':
#    env_path = Path('../..') / '.env'
#else:
#    env_path = Path('.') / '.env'
#
#load_dotenv(dotenv_path=env_path)

HOST_INFLUX=os.environ.get("HOST_INFLUX")
PORT_INFLUX=os.environ.get("PORT_INFLUX")

client_influx =InfluxDBClient(host=HOST_INFLUX,port=PORT_INFLUX)
client_df = DataFrameClient(host=HOST_INFLUX, port=PORT_INFLUX,
        database='db_ereal')
