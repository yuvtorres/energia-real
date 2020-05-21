import time
import atexita

# Modules ad-hoc from e-real
import src.config
from src.model import pronostico
from src.model  import cluster
from src.get_data import tool_esios as t_esios
from src.get_data import analisis_ree as a_ree
from src.get_data import carga_influx as c_ix
from src.get_data import carga_esios as c_esios
from src.get_data import carga_aemet as c_aemet

from apscheduler.schedulers.background import BackgroundScheduler


def update_data_from_esios_aemet():
    t_esios.lee_esios_carga_influx(551)
    t_esios.lee_esios_carga_influx(1295)
    c_aemet.c_aemet_actual()


scheduler = BackgroundScheduler()
scheduler.add_job(func=update_data_from, trigger="interval", seconds=3600)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
