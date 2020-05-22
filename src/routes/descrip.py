from src.app import app
from src.connect_db import client_mongo
from src.get_data import describ_db
from src.model import cluster
from bson.json_util import dumps
import json
import pandas as pd

### Module makes the query of the description and estaciones

@app.route("/bd_description/")
def description():
    describ_db.describ_db()
    db=client_mongo.ereal_collections
    description=db.descrip.find( { } ,{"_id":0,"name":1,"f_data":1,"l_data":1})
    description='{"description":'+dumps(description)+'}'
    description_j=json.loads(description)
    return description_j


@app.route("/estaciones/")
def estationes():
    df=pd.read_csv('data/estaciones.csv')
    estaciones=df[['lat','lon']].div(10000).T.to_dict('dict')
    estaciones='{"estaciones":'+dumps(estaciones)+'}'
    estaciones_j=json.loads(estaciones)
    return estaciones_j



