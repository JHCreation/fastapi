from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import select, or_, and_, not_, func
from fastapi import APIRouter, HTTPException, Response, Request
from starlette import status

def qryTree(node, model):
    print(type(node),node['id'])
    if(node['type'] == 'group'):
        qry= []
        
        for filter in node['filter']:
            res= qryTree(filter, model)
            qry.append(res)
        # print('qry::',qry)
        if(node['operator'].upper() =='AND' ):
            group= and_(*qry)
            # print(str(group.compile(compile_kwargs={"literal_binds": True})), 'and', group)
            return group
            
        if(node['operator'].upper() =='OR' ):
            group= or_(*qry)
            # group= or_(*qry).self_group()
            # print(str(group.compile(compile_kwargs={"literal_binds": True})), 'or', group)
            return group
        
    else:
        # print('arrive filter', node['id'], model, node['key'])
        key= getattr(model, node['key'])
        where= key == node['value']
        option= node['option'].upper()
        if option == "=":
            where= key == node['value']
        elif option == "!=":
            where = key != node['value']
        elif option == ">":
            where = key > node['value']
        elif option == ">=":
            where = key >= node['value']
        elif option == "<":
            where = key < node['value']
        elif option == "<=":
            where = key <= node['value']
        elif option == "LIKE":
            where = key.like(f"%{node['value']}%")
        elif option == "NOTLIKE":
            where = not_(key.like(f"%{node['value']}%"))
        elif option == "LIKE%":
            where = key.like(f"{node['value']}%")
        elif option == "%LIKE":
            where = key.like(f"%{node['value']}")
        elif option == "IN":
            where = key.in_(node['value'])
        elif option == "ISNULL":
            where = key == None
        elif option == "NOTISNULL":
            where = not_(key == None)
        else:
            where = None
        
        # print(where, type(where), model.__tablename__, node['id'])
        return where

def get_list_all(model, db: Session):
    data = db.scalars(select(model)
                            .order_by(model.id.desc()))
    total = db.scalar(select(func.count()).select_from(model))
    list = data.all()
    return total, list

def get_list(model, db: Session, skip: int = 0, limit: int = 10, filter=None):
    # test= or_(model.key=='test', model.name=='name', 
    #            or_(model.status=='status', model.value.like('%value%'), model.key=='key-value', model.key.in_(['s','aa'])).self_group()).self_group()
    # print('test:',test)
    # return
    selected= select(model)
    if( filter ):
        where= qryTree(filter, model)
        selected= select(model).where(where)
        # print(str(selected.compile(compile_kwargs={"literal_binds": True})))

    qry= selected\
        .offset(skip).limit(limit)\
        .order_by(model.id.desc())
    data = db.scalars(qry)
    print(str(qry.compile(compile_kwargs={"literal_binds": True})))
    
    total = db.scalar(select(func.count()).select_from(selected))
    # total = db.select([db.func.count()]).select_from(selected).scalars()
    list = data.all()
    return total, list  # (전체 건수, 페이징 적용된 질문 목록)

def create(model, db: Session, param, res_id="id", update=None):
    
    param= param.model_dump()
    if update != None:
        param.update(update)
    data = model(**param)
   
    db.add(data)
    db.commit()
    db.refresh(data)
    print('db저장 완료!')
    return { 
        res_id: getattr(data, res_id),
        'status': 'success'
    }

async def asyncCreate(model, db: Session, param, res_id="id", update=None):
    print('db 저장 시작')
    
    param= param.model_dump()
    if update != None:
        param.update(update)
    data = model(**param)
   
    db.add(data)
    await db.commit()
    await db.refresh(data)
    print('db저장 완료!')
    return { 
        res_id: getattr(data, res_id),
        'status': 'success'
    }
async def aync_get_list_all(model, db: Session):
    data = await db.scalars(select(model)
                            .order_by(model.id.desc()))
    total = await db.scalar(select(func.count()).select_from(model))
    list = data.all()
    return total, list
def get_item(model, db: Session, key: str, value: str):
    print('get_item', key, value)
    return db.query(model).filter(getattr(model, key) == value)

def update(model, db: Session, param, filter_key='id', filter_value='', res_id="id", update=None):
    param= param.model_dump(exclude_unset=True)
    datas = get_item(model, db, key=filter_key, value=filter_value)
    data= datas.first()
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if update != None:
        param.update(update)

    update_query = datas.update(
        param,
        synchronize_session="evaluate"
    )
    # print(update_query.statement.compile(compile_kwargs={"literal_binds": True}))
    db.commit()
    return { 
        res_id: getattr(data, res_id),
        'status': 'success'
    }