from fastapi import APIRouter, HTTPException, Request, Depends, Body, Security
from datetime import datetime, UTC
from sqlalchemy.ext.asyncio import AsyncSession
from ...database import get_async_db
from ...config import logger
from .._comm import comm_schema, comm_crud
from ...models import Category
from .category_schema import CategorysCreate, CategorysUpdate, CategorysBase
from .._auth.auth import api_bearer_token


ALLOWED_ORIGINS = ["http://localhost:5173", "https://mapoclean.com", "https://www.mapoclean.com"]
async def check_domain_auth(request: Request):
    print('마포크린 요청 호스트 검사', request.headers.get("origin"))
    if request.headers.get("origin") not in ALLOWED_ORIGINS:
        raise HTTPException(status_code=403, detail="Not authorized")

router = APIRouter(
    # allow_origins=["*"],
    prefix="/api/web/category",
    tags=["web 공통 category"],
    # dependencies=[Depends(check_domain_auth)],
)

@router.get("/list")
async def category_list(
    # db: Annotated[AsyncSession, Depends(get_async_db)], 
    db: AsyncSession = Depends(get_async_db),
    params: comm_schema.CommFilterList = Depends(),
):
    logger.debug(params)
    total, list= await comm_crud.async_get_list(Category, db, skip=params.skip, limit=params.limit)
    return {
        "total": total,
        "list": list
    }

@router.post("/create")
async def create_works(
    item: CategorysCreate,
    # item: CategorysBase = Body(...),

    # item: category_schema.CampaignCreate= Depends(),
    db: AsyncSession = Depends(get_async_db),
    api_key: str = Security(api_bearer_token)
):
    logger.debug(item)
    update= {
        'create_date' : datetime.now(),
    }
    return await comm_crud.async_create(Category, db, item, res_id='id', update=update)

@router.put("/update/{id}")
async def update_works(
    id: str,
    # params: CategorysBase,
    db: AsyncSession = Depends(get_async_db),
    params: CategorysBase = Body(...),
):
    update= {
        'modify_date' : datetime.now(),
    }
    return await comm_crud.async_update(Category, db, params, filter_key='id', filter_value=id, res_id='id', update=update)

@router.delete("/delete/{id}")
async def delete_works(
    id: str,
    # item: WorksUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    # print(item)
    # return
    return await comm_crud.async_delete(Category, db, filter_key='id', filter_value=id, res_id='id')