from src.app import app
from src.connect_db import client_mongo
from src.model import cluster
from src.model import pronostico
from bson.json_util import dumps
import json


### Module with endpoints of forecast

# Endpoint for calculation of all forecast wind and generation
@app.route("/forecast_eo_all/")
def forecast_eo_calc():
    try:
        cluster.make_winds()
    except:
        cluster.crea_cluster()
        cluster.make_winds()

    pronostico.make_gen_eo()

    db=client_mongo.ereal_collections

    r2=db.scores.find({},{})

    return {'result':r2}

# Endpoint for calculation of the forecast of the generation
@app.route("/forecast_eo")
def forecast_eo():
    pronostico.make_gen_eo()
    db=client_mongo.ereal_collections
    r2=db.scores.find({'name':'eolico'},{'_id':0,'r2':1})
    return {'r2':r2}


# Endpoint for calculation of the cluster
@app.route("/crea_cluster")
def ep_crea_cluster():
    cluster.crea_cluster()
    db=client_mongo.ereal_collections
    r2=db.scores.find({'name':'eolico'},{'_id':0,'r2':1})
    return {'r2':r2}



