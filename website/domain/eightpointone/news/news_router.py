from datetime import timedelta, datetime, UTC
from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security, Form, Body, Query
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from ..eightpointone_router import router
from ..._comm import comm_schema, comm_crud

from ....database import get_async_db
from ....model.eightpointone.eightpointone_model import News
from ....config import logger, ROOT_DIR
from .news_schema import NewsCreate, NewsBase, NewsUpdate, NewsDeletes
from ...files import files_crud
from ..eightpointone_router import DOMAIN_NAME
from ..._auth.auth import api_bearer_token
from typing import List
import os
import uuid
from dotenv import load_dotenv
load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)

UPLOAD_PATH= os.environ.get('UPLOAD_PATH')
UPLOADS_PATH= f"{UPLOAD_PATH}"
route_name="news"

router = APIRouter(
    prefix=f"/{route_name}",
    tags=[f"epo/{route_name}"],

)

@router.get("/list")
async def list(
    # db: Annotated[Session, Depends(get_async_db)], 
    db: AsyncSession = Depends(get_async_db),
    params: comm_schema.CommFilterList = Depends(),
):
    logger.debug(params, News)
    total, list= await comm_crud.async_get_list(News, db, skip=params.skip, limit=params.limit)
    return {
        "total": total,
        "list": list
    }

@router.post("/create")
async def create(
    item: NewsCreate,
    db: AsyncSession = Depends(get_async_db),
    api_key: str = Security(api_bearer_token)
):
    # logger.debug(f"마포크린 works : {item}")
    update= {
        'create_date' : datetime.now(),
    }
    return await comm_crud.async_create(News, db, item, res_id='id', update=update)

@router.put("/update/{id}")
async def update(
    id: str,
    db: AsyncSession = Depends(get_async_db),
    params: NewsBase = Body(...),
    api_key: str = Security(api_bearer_token)
):
    update= {
        'modify_date' : datetime.now(),
    }
    return await comm_crud.async_update(News, db, params, filter_key='id', filter_value=id, res_id='id', update=update)

@router.delete("/delete/{id}")
async def delete(
    id: str,
    db: AsyncSession = Depends(get_async_db),
    api_key: str = Security(api_bearer_token)

):
    # print(item)
    # return
    return await comm_crud.async_delete(News, db, filter_key='id', filter_value=id, res_id='id')
 

@router.delete("/deletes")
async def works_deletes(
    param: NewsDeletes,
    # ids: List[int]= Query(...),
    db: AsyncSession = Depends(get_async_db),
    api_key: str = Security(api_bearer_token)
):
    # logger.debug(f"{UPLOAD_PATH, DOMAIN_NAME, param.ids}")
    files_crud.delete_multiple_files(f"{UPLOAD_PATH}/{DOMAIN_NAME}/{route_name}", param.ids)
    return await comm_crud.async_deletes(News, db, filter_key='key', filter_value=param.ids)