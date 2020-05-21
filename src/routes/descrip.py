from src.app import app
from src.connect_db import client_mongo
from bson.json_util import dumps
import json


### Module of the chats funcionalities

## makes the query of all chats
@app.route("/bd_description/")
def description():
    db=client_mongo.ereal_collections
    description=db.description.find( { } ,{"_id":0,"chat":1})
    description='{"description":'+dumps(chats)+'}'
    description_j=json.loads(description)
    return description_j

