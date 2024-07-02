import os
from urllib.parse import quote, quote_plus
from dotenv import load_dotenv
load_dotenv()

USERNAME= os.environ.get('DB_USERNAME')
PASSWORD= os.environ.get('DB_PASSWORD')
ENCORD_PW= quote_plus(PASSWORD)
HOST= os.environ.get('DB_HOST')
PORT= os.environ.get('DB_PORT')
DBNAME= os.environ.get('DB_NAME')
DB_URL= os.environ.get('DB_URL')
DB_URL_ASYNC= os.environ.get('DB_URL_ASYNC')


DATABASE_URL = f"mysql+pymysql://{USERNAME}:{ENCORD_PW}@{HOST}:{PORT}/{DBNAME}"
DATABASE_URL_ASYNC = f"mysql+aiomysql://{USERNAME}:{ENCORD_PW}@{HOST}:{PORT}/{DBNAME}"
# DATABASE_URL = DB_URL
# DATABASE_URL_ASYNC = DB_URL_ASYNC