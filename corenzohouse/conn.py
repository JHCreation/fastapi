import os
from urllib.parse import quote, quote_plus
from dotenv import load_dotenv
from . import config

USERNAME= os.environ.get('DB_USERNAME')
PASSWORD= quote_plus(os.environ.get('DB_PASSWORD'))
ENCORD_PW= PASSWORD.replace('%', '%%')
HOST= os.environ.get('DB_HOST')
PORT= os.environ.get('DB_PORT')
DBNAME= os.environ.get('DB_NAME')
DB_URL= os.environ.get('DB_URL')
DB_URL_ASYNC= os.environ.get('DB_URL_ASYNC')

DATABASE_URL = f"mysql+pymysql://{USERNAME}:{ENCORD_PW}@{HOST}:{PORT}/{DBNAME}"
DATABASE_URL_CONN = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
DATABASE_URL_ASYNC = f"mysql+aiomysql://{USERNAME}:{ENCORD_PW}@{HOST}:{PORT}/{DBNAME}"
DATABASE_URL_ASYNC_CONN = f"mysql+aiomysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"