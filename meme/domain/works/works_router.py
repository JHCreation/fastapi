import os
from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security
from fastapi.encoders import jsonable_encoder

from meme.database import get_db
from . import works_schema
from meme.domain._comm import comm_crud, comm_schema
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status
from ...domain.user.user_auth import api_bearer_token
import time
import httpx

db= os.environ.get('DB_NAME')
router = APIRouter(
    prefix="/api/works",
    tags=["meme works"]
)
# print(oauth2_scheme.__dir__())
from ...model.works import Works

@router.get("/test")
async def make_async_request():
    """비동기 방식으로 외부 API 호출 test"""
    try:
        # 비동기 방식 요청
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8000/api/works/list")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create")
def create(
    item: works_schema.WorksCreate,
    # item: category_schema.CampaignCreate= Depends(),
    db: Session = Depends(get_db),
    api_key: str = Security(api_bearer_token)
):  
    # category = category_crud.get_existing_category(db, category_create=item)
    # if category:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                         detail="이미 존재하는 카테고리입니다.")
    update= {
        'create_date' : datetime.now(),
    }
    return comm_crud.create(Works, db, item, res_id='id', update=update)

@router.put("/update/{id}")
def update(
    # item,
    id: int,
    item: works_schema.WorksCreate,
    # item: category_schema.CampaignCreate= Depends(),
    db: Session = Depends(get_db),
    api_key: str = Security(api_bearer_token)
):  
    # update= {
    #     'create_date' : datetime.now(),
    # }
    return comm_crud.update(Works, db, item, filter_key='id', filter_value=id, res_id='key')

@router.get("/list", response_model=works_schema.WorksList)
def list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10):
    total, list = comm_crud.get_list(
        Works, db, skip=page*size, limit=size)
    
    # time.sleep(5)
    # print('lisssssssss')
    return {
        'total': total,
        'list': list
    }

@router.get("/{id}",)
def list( id: int, db: Session = Depends(get_db) ):
    datas = comm_crud.get_item(
        Works, db, key='id', value=id)
    data= datas.first()
    # time.sleep(5)
    return data
    # print('lisssssssss')
    return {
        'total': total,
        'list': list
    }


@router.post("/list", 
            #  response_model=category_schema.CategoryList
            )
def list(item:comm_schema.CommFilterList,
                  db: Session = Depends(get_db),
                  ):
    page, size, filter= item
    page= page[1]
    size= size[1]
    filter= filter[1]
    filters= eval(filter)
    # print(filter)

    total, list = comm_crud.get_list(
        Works, db, skip=page*size, limit=size, filter=filters)
    
    return {
        'total': total,
        'list': list
    }