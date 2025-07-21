from datetime import datetime, UTC
from fastapi import APIRouter
from fastapi import Depends, Security, Form, Body, Query
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from ..mapoclean_router import router
from ..._comm import comm_schema, comm_crud

from ....database import get_async_db
from ....model.mapoclean.mapoclean_works import Works
from ....config import logger, ROOT_DIR
from .works_schema import WorksCreate, WorksBase, WorksDeletes
from ...files import files_crud
from ..mapoclean_router import DOMAIN_NAME
from ..._auth.auth import api_bearer_token
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)

ROOT_PATH= os.environ.get('ROOT_PATH')
UPLOAD_PATH= os.environ.get('UPLOAD_PATH')
UPLOADS_PATH= f"{UPLOAD_PATH}"
route_name="works"
router = APIRouter(
    prefix=f"/{route_name}",
    # tags=["mapoclean/works"]
)

@router.get("/list")
async def list(
    # db: Annotated[Session, Depends(get_async_db)], 
    db: AsyncSession = Depends(get_async_db),
    params: comm_schema.CommFilterList = Depends(),
):
    logger.debug(params)
    total, list= await comm_crud.async_get_list(Works, db, skip=params.skip, limit=params.limit)
    return {
        "total": total,
        "list": list
    }

@router.post("/create")
async def create_works(
    item: WorksCreate,
    db: AsyncSession = Depends(get_async_db),
    api_key: str = Security(api_bearer_token)
):
    update= {
        'create_date' : datetime.now(),
    }
    return await comm_crud.async_create(Works, db, item, res_id='id', update=update)

@router.put("/update/{id}")
async def update_works(
    id: str,
    db: AsyncSession = Depends(get_async_db),
    params: WorksBase = Body(...),
    api_key: str = Security(api_bearer_token)
):
    update= {
        'modify_date' : datetime.now(),
    }
    return await comm_crud.async_update(Works, db, params, filter_key='id', filter_value=id, res_id='id', update=update)

@router.delete("/delete/{id}")
async def delete_works(
    id: str,
    db: AsyncSession = Depends(get_async_db),
    api_key: str = Security(api_bearer_token)

):
    return await comm_crud.async_delete(Works, db, filter_key='id', filter_value=id, res_id='id')
 

@router.delete("/deletes")
async def works_deletes(
    param: WorksDeletes,
    # ids: List[int]= Query(...),
    db: AsyncSession = Depends(get_async_db),
    api_key: str = Security(api_bearer_token)
):
    # logger.debug(f"{UPLOAD_PATH, DOMAIN_NAME, param.ids}")
    files_crud.delete_multiple_files(f"{UPLOAD_PATH}/{DOMAIN_NAME}/{route_name}", param.ids)
    return await comm_crud.async_deletes(Works, db, filter_key='key', filter_value=param.ids)