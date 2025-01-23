import os
from urllib.parse import quote, quote_plus
from dotenv import load_dotenv

# from config import ROOT_DIR
current_file_path = os.path.abspath(__file__)
ROOT_DIR=os.path.dirname(current_file_path)
print(current_file_path, ROOT_DIR,)

# DB_NAME_1= os.environ.get('DB_NAME_1')
THIS_DIR= os.environ.get('ROOT_DIR_1')
load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)
# print(DB_NAME_1, 'first')
print(THIS_DIR, 'first!', os.environ.get('DB_NAME'), os.getcwd(), f'{ROOT_DIR}/.env')

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
# DATABASE_URL = DB_URL
# DATABASE_URL_ASYNC = DB_URL_ASYNC