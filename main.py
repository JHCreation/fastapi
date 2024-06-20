import os
import json
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.files import files_router
from domain.category import category_router
from domain.campaign import campaign_router
from domain.question import question_router
from domain.answer import answer_router
from domain.user import user_router



app = FastAPI()
origins = json.loads(os.environ.get('CORS_ORIGIN'))
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.include_router(campaign_router.router)
app.include_router(category_router.router)
app.include_router(files_router.router)



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