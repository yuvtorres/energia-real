from src.config import PORT
from src.app import app
import src.get_data import analisis_ree
import src.routes.home

app.run("0.0.0.0", PORT, debug=True)
