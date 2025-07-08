import os
from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security
from fastapi.encoders import jsonable_encoder

from meme.database import get_db, get_async_db
from meme.domain.category import category_crud, category_schema
from meme.domain._comm import comm_crud, comm_schema
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status
from meme.domain.user.user_auth import api_bearer_token
import time

from ..logger import logging

db= os.environ.get('DB_NAME')
router = APIRouter(
    prefix="/api/category",
)
# print(oauth2_scheme.__dir__())
from meme.models import Category



@router.put("/update/{id}")
async def category_update(
    # item,
    id: str,
    item: category_schema.CategoryCreate,
    # item: category_schema.CampaignCreate= Depends(),
    # db: Session = Depends(get_db),
    db: Session = Depends(get_async_db),
    api_key: str = Security(api_bearer_token)
):  
    update_data = item.model_dump(exclude_unset=True)
    print(item)
    # return

    update= {
        'modify_date' : datetime.now(),
    }
    return await comm_crud.asyncUpdate(Category, db, params=item, filter_key='key', filter_value=id, res_id='key', update=update)

    return category_crud.update_category(db, update_data, id=id)

@router.post("/create")
def category_create(
    item: category_schema.CategoryCreate,
    # item: category_schema.CampaignCreate= Depends(),
    db: Session = Depends(get_db),
    api_key: str = Security(api_bearer_token),
):  
    logging.debug(item)
    category = category_crud.get_existing_category(db, category_create=item)
    if category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 카테고리입니다.")
    return category_crud.create_category(db, item)

@router.delete("/delete/{id}")
def category_delete(id: int, 
                    # _question_delete: category_schema.CategoryDelete,
                    db: Session = Depends(get_db),
                    # current_user: User = Depends(get_current_user)
                    # api_key: str = Security(api_bearer_token)
                    ):
    # print('api_key',api_key)
    # return
    # db_question = category_crud.get_category(db, question_id=_question_delete.question_id)
    # if not db_question:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail="데이터를 찾을수 없습니다.")
    # if current_user.id != db_question.user.id:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail="삭제 권한이 없습니다.")
    # question_crud.delete_question(db=db, db_question=db_question)
    return category_crud.delete_categroy(db, id=id)

@router.delete("/deletes")
def category_deletes(
    _category_deletes: category_schema.CategoryDeletes,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
    api_key: str = Security(api_bearer_token)
):
    # print('api_key',api_key)
    # return
    # db_question = category_crud.get_category(db, question_id=_question_delete.question_id)
    # if not db_question:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail="데이터를 찾을수 없습니다.")
    # if current_user.id != db_question.user.id:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail="삭제 권한이 없습니다.")
    # question_crud.delete_question(db=db, db_question=db_question)

    return category_crud.deletes_categroy(db, ids=_category_deletes)

@router.get("/list", response_model=category_schema.CategoryList)
def category_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10):
    total, list = comm_crud.get_list(
        Category, db, skip=page*size, limit=size)
    
    # time.sleep(5)
    # print('lisssssssss')
    return {
        'total': total,
        'list': list
    }


    

@router.post("/list", 
            #  response_model=category_schema.CategoryList
            )
def category_list(item:comm_schema.CommFilterList,
                  db: Session = Depends(get_db),
                  ):
    page, size, filter= item
    page= page[1]
    size= size[1]
    filter= filter[1]
    filters= eval(filter)
    # print(filter)

    total, list = comm_crud.get_list(
        Category, db, skip=page*size, limit=size, filter=filters)
    
    return {
        'total': total,
        'list': list
    }


@router.get("/list-all", response_model=category_schema.CategoryList)
def category_list(db: Session = Depends(get_db)):
    total, list = comm_crud.get_list_all(
        Category, db)
    return {
        'total': total,
        'list': list
    }
