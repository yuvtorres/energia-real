from src.app import app
from src.connect_db import client_mongo
from src.get_data import describ_db
from bson.json_util import dumps
import json


### Module makes the query of the description

@app.route("/bd_description/")
def description():
    describ_db.describ_db() 
    db=client_mongo.ereal_collections
    description=db.descrip.find( { } ,{"_id":0,"name":1,"f_data":1,"l_data":1})
    description='{"description":'+dumps(description)+'}'
    description_j=json.loads(description)
    return description_j

