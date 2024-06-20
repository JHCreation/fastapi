from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security
from fastapi.encoders import jsonable_encoder

from database import get_db
from domain.category import category_crud, category_schema
from domain._comm import comm_crud, comm_schema
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status
from domain.user.user_auth import api_bearer_token

router = APIRouter(
    prefix="/api/category",
)
# print(oauth2_scheme.__dir__())
from models import Category


@router.put("/update/{id}")
def category_update(
    # item,
    id: int,
    item: category_schema.CategoryCreate,
    # item: category_schema.CampaignCreate= Depends(),
    db: Session = Depends(get_db),
    api_key: str = Security(api_bearer_token)
):  
    # print(api_key)
    update_data = item.model_dump(exclude_unset=True)
    return category_crud.update_category(db, update_data, id=id)

@router.post("/create")
def category_create(
    item: category_schema.CategoryCreate,
    # item: category_schema.CampaignCreate= Depends(),
    db: Session = Depends(get_db),
    api_key: str = Security(api_bearer_token)
):  
    category = category_crud.get_existing_category(db, category_create=item)
    if category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 카테고리입니다.")
    return category_crud.create_category(db, item)

    

@router.get("/list", response_model=category_schema.CategoryList)
def category_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10):
    total, list = comm_crud.get_list(
        Category, db, skip=page*size, limit=size)
    return {
        'total': total,
        'category_list': list
    }


    

@router.post("/list", response_model=category_schema.CategoryList )
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
        'category_list': list
    }


@router.get("/list-all", response_model=category_schema.CategoryList)
def category_list(db: Session = Depends(get_db)):
    total, list = comm_crud.get_list_all(
        Category, db)
    return {
        'total': total,
        'category_list': list
    }
