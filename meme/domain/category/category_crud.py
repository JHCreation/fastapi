from sqlalchemy.orm import Session
from meme.domain.category.category_schema import CategoryCreate, CategoryUpdate
from meme.models import Category
from datetime import datetime
from sqlalchemy import select, func, or_
from starlette import status
from fastapi import APIRouter, HTTPException, Response, Request
import json

import logging

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def modify_category(db: Session, db_category: Category,
                    category_update, id):
    # db_category.subject = category_update.subject
    # db_category.content = category_update.content
    db_category.create_date = datetime.now()
    db.add(db_category)
    db.commit()



def update_category(db: Session, category_update, id):
    db_category = get_category(db, id=id)
    get_data= db_category.first()
    if not get_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    category_update.update({'modify_date' : datetime.now()})
    # print('update', category_update)
    update_query = db_category.update(
        category_update,
        synchronize_session="evaluate"
    )
    # print(update_query.statement.compile(compile_kwargs={"literal_binds": True}))
    db.commit()
    return { 
        'id': id,
        'status': 'success'
    }
    


def create_category(db: Session, category_create: CategoryCreate):
    # print(category_create.model_dump())
    param= category_create.model_dump()
    param.update({ 
        'create_date' : datetime.now(), 
        'modify_date' : datetime.now() 
    })
    db_category = Category(**param)
   
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return { 
        'id': db_category.id,
        'status': 'success'
    }

def get_existing_category(db: Session, category_create: CategoryCreate):
    return db.query(Category).filter(
        (Category.key == category_create.key)
    ).first()

def get_category(db: Session, id: str):
    return db.query(Category).filter(Category.id == id)

def delete_categroy(db: Session, id:str):
    db_category = get_category(db, id=id)
    get_data= db_category.first()
    if not get_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    print('delete', id, db_category, get_data)
    db_category.delete()
    db.commit()
    return { 'id': id, 'status': 'success' }

def deletes_categroy(db: Session, ids:str):
    
    print('ids', ids, json.loads(ids.ids),  Category.id.in_(json.loads(ids.ids)))
    db_category= db.query(Category).filter(
        Category.id.in_(json.loads(ids.ids))
    )
    get_data= db_category.all()
    if not get_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    db_category.delete()
    db.commit()
    return { 'id': ids, 'status': 'success' }