from influxdb import InfluxDBClient
from influxdb import DataFrameClient
from pymongo import MongoClient
from src.config import PORT_INFLUX
from src.config import HOST_INFLUX
from src.config import PORT_MONGO
from src.config import HOST_MONGO

import src.config
import os

client_influx =InfluxDBClient(host=HOST_INFLUX,port=PORT_INFLUX)
client_df = DataFrameClient(host=HOST_INFLUX, port=PORT_INFLUX,
        database='db_ereal')

client_mongo = MongoClient(HOST_MONGO,PORT_MONGO)
