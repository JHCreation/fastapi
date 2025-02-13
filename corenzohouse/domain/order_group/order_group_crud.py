from sqlalchemy.orm import Session
from ...model.orders import OrderGroup
from sqlalchemy.future import select


# async def order_group_get_item(
#         db: Session, min_date: int = None, max_date: int = None,
#         tid: str = None, oid: str = None, sid: str = None, status: str = None
#     ):

#     query = select(OrderGroup)

#     if min_date:
#         query = query.where(OrderGroup.create_date >= min_date)
#     if max_date:
#         query = query.where(OrderGroup.create_date <= max_date)
#     if tid:
#         query = query.where(OrderGroup.table_id == tid)
#     if oid:
#         query = query.where(OrderGroup.order_id == oid)
#     if sid:
#         query = query.where(OrderGroup.store_id == sid)
#     if status:
#         query = query.where(OrderGroup.status == status)

    
#     print(f"Generated Query: {str(query)}")
#     query= query.order_by(OrderGroup.id.desc())
#     result= await db.execute(query)
#     order = result.scalars().first()
    
#     return order

def order_group_get(
        params: dict
    ):
    query = select(OrderGroup)

    if params.get('min_date') is not None:
        query = query.where(OrderGroup.create_date >= params['min_date'])
    if params.get('max_date') is not None:
        query = query.where(OrderGroup.create_date <= params['max_date'])
    if params.get('sale_date') is not None:
        query = query.where(OrderGroup.sale_date == params['sale_date'])
    if params.get('tid') is not None:
        query = query.where(OrderGroup.table_id == params['tid'])
    if params.get('oid') is not None:
        query = query.where(OrderGroup.order_id == params['oid'])
    if params.get('sid') is not None:
        query = query.where(OrderGroup.store_id == params['sid'])
    if params.get('status') is not None:
        query = query.where(OrderGroup.status == params['status'])

    return query

async def order_group_get_item(
        db: Session, params: dict
    ):
    query= order_group_get(params)
    
    print(f"Generated Query: {str(query)}")
    query= query.order_by(OrderGroup.id.desc())
    result= await db.execute(query)
    order = result.scalars().first()
    
    return order


async def order_group_get_list(
        db: Session, params: dict
    ):
    
    query= order_group_get(params)
    query= query.order_by(OrderGroup.id.desc())
    result= await db.execute(query)
    order = result.scalars().all()
    
    return order

