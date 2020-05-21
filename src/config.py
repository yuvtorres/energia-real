from pathlib import Path
from dotenv import load_dotenv
import os

last_dir=os.getcwd().split('/')[-1]

if last_dir=='src':
    env_path = Path('..') / '.env'
elif last_dir=='get_data':
    env_path = Path('../..') / '.env'
else:
    env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

PORT_MONGO = int(os.getenv("PORT_MONGO"))
PORT_INFLUX = int(os.getenv("PORT_INFLUX"))
HOST_INFLUX = os.getenv("HOST_INFLUX")
HOST_MONGO = os.getenv("HOST_MONGO")
AEMET_KEY = os.getenv("AEMET_KEY")
REE_KEY = os.getenv("REE_KEY")
PORT=os.getenv("PORT")
