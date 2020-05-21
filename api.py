from src.config import PORT
from src.app import app

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

# import routes of app
import src.routes.home
import src.routes.descrip
import src.routes.forecast
app.run("0.0.0.0", PORT, debug=True)
