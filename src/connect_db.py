# File for configuration of the connections with Infludb and MongoDB.
from influxdb_client import InfluxDBClient, Point
from pymongo import MongoClient
from src.config import PORT_INFLUX
from src.config import HOST_INFLUX
from src.config import USER_INFLUX
from src.config import PASSWORD_INFLUX
from src.config import TOKEN_INFLUX
from src.config import PORT_MONGO
from src.config import HOST_MONGO

import src.config
import os

client_influx =InfluxDBClient(url='http://'+str(HOST_INFLUX)+':'+str(PORT_INFLUX),token=TOKEN_INFLUX)
client_mongo = MongoClient(HOST_MONGO,PORT_MONGO)
