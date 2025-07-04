from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import select, or_, and_, not_, func, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import APIRouter, HTTPException, Response, Request
from starlette import status
import json
from ...config import logger
from ...lib import format

def qryTree(node, model):
    # print(type(node),node['id'])
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


async def async_get_list(model, db: Session, skip: int = None, limit: int = None, filter=None):
    total_stmt = select(func.count()).select_from(model)
    total_result = await db.execute(total_stmt)
    total = total_result.scalar_one()
    
    selected= select(model)
    if( filter ):
        where= qryTree(filter, model)
        selected= select(model).where(where)

    stmt= selected\
        .offset(skip).limit(limit)\
        .order_by(model.id.desc())

    compiled_query = stmt.compile(compile_kwargs={"literal_binds": True})
    logger.debug(f"get list query: {str(compiled_query)}")
    result = await db.execute(stmt)
    list= result.scalars().all()
    return total, list



async def async_create(model, db: Session, param, res_id="id", update=None):
    logger.debug('db 저장 시작')
    
    if not isinstance(param, dict): 
        param= param.model_dump(exclude_unset=True, exclude_none=True)
    
    param= format.makeToString(param)
    # for key, value in param.items():
    #     logger.debug(f'Key: {key}, Value: {value}, Type: {type(value)}')
    #     if not isinstance(value, (str, type(None))):
    #         param[key]= json.dumps(value)
    
    if update != None:
        param.update(update)
    data = model(**param)
    db.add(data)

    try:
        await db.commit()
        await db.refresh(data)
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="데이터 무결성 오류가 발생했습니다. (중복된 키 또는 필수 필드 누락)"
        ) from e
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="데이터베이스 저장 중 오류가 발생했습니다."
        ) from e
    # await db.commit()
    # await db.refresh(data)
    logger.debug('db저장 완료!')
    return { 
        res_id: getattr(data, res_id),
        'status': 'success'
    }



def get_item_query(model, key: str, value: str):
    return select(model).where(getattr(model, key) == value)

async def async_get_item(model, db: Session, key: str, value: str):
    stmt= get_item_query(model, key, value)
    result= await db.execute(stmt)
    item = result.scalar_one_or_none()
    return item


async def async_update(model, db: Session, params, filter_key='id', filter_value='', res_id="id", update=None):


    if not isinstance(params, dict): 
        params= params.model_dump(exclude_unset=True, exclude_none=True)
    
    params= format.makeToString(params)
    # for key, value in param.items():
    #     logger.debug(f'Key: {key}, Value: {value}, Type: {type(value)}')
    #     if not isinstance(value, (str, type(None))):
    #         param[key]= json.dumps(value)
    
    # if update != None:
    #     update_data.update(update)
    # update_data = model(**params)


    # update_data = params.model_dump(exclude_unset=True, exclude_none=True)  # None이 아닌 값만 필터링'
    # update_data= format.makeToString(update_data)
    query = get_item_query(model, key=filter_key, value=filter_value)
    
    result= await db.execute(query)
    # data = result.scalars().first() 
    data = result.scalar_one_or_none()
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if update != None:
        params.update(update)

    # ✅ 2. 전달된 데이터 순회하면서 None이 아닌 값만 업데이트
    for key, value in params.items():
        setattr(data, key, value)  # 동적으로 속성 업데이트
    await db.commit()
    await db.refresh(data)
    return { 
        res_id: getattr(data, res_id),
        'status': 'success'
    }


async def async_delete(model, db: Session, filter_key='id', filter_value='', res_id="id", update=None):
    stmt = delete(model).where(getattr(model, filter_key) == filter_value)
    # 쿼리 출력
    # compiled_query = stmt.compile(compile_kwargs={"literal_binds": True})
    # print("Executing query:", str(compiled_query))
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount


async def async_deletes(model, db: AsyncSession, filter_key='id', filter_value=''):
    logger.debug(f'{filter_key}, {filter_value}')
    # return 
    if not filter_value:
        raise HTTPException(status_code=400, detail="No IDs provided")
    key= getattr(model, filter_key)

    stmt = delete(model).where(key.in_(filter_value))
    result= await db.execute(stmt)
    await db.commit()
    return {
        "result": result.rowcount,
        'status': 'success'
    }
