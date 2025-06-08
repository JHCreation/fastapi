import os
import json
from dotenv import load_dotenv
# from config import ROOT_DIR
current_file_path = os.path.abspath(__file__)
ROOT_DIR=os.path.dirname(current_file_path)


from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Response, Request


def get_allowed_origins(origin):
    print(origin)
    if origin.endswith(".example.com"):
        return [origin]
    return []

app = FastAPI()
import corenzohouse.route
import meme.route
import website.route
# 얘네들이 실행되면서 load_dotenv(override)도 같이 덮어버리니 주의(순서)!

# logging.debug("디버그 정보")
# logging.error(os.environ.get('ENV'))
load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)
# logging.info(ROOT_DIR, 'start!!!',' 2start')
# print(ROOT_DIR)
# logging.error(os.environ.get('CORS_ORIGIN'))
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)
# print(log_level, '???')
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    logger.error(f"Request body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": (await request.body()).decode()},
    )

if __name__ == 'main':
    origins = json.loads(os.environ.get('CORS_ORIGIN'))
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[],
        allow_origins=origins,
        # allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # allow_origin_func=get_allowed_origins,
    )
    



# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_price": item.price, "item_id": item_id}