from influxdb import InfluxDBClient
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('../..') / '.env'
load_dotenv(dotenv_path=env_path)

HOST_INFLUX=os.environ.get("HOST_INFLUX")
PORT_INFLUX=os.environ.get("PORT_INFLUX")
client_influx =InfluxDBClient(host=HOST_INFLUX,port=PORT_INFLUX)

