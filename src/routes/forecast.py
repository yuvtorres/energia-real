from src.app import app
from src.connect_db import client_mongo
from src.model import cluster
from bson.json_util import dumps
import json


### Module makes the query of the description

@app.route("/forecast_eo/")
def forecast_eo():
    try:
        r2=cluster.make_winds()
    except:
        cluster.crea_cluster()
        r2=cluster.make_winds()
    return r2

