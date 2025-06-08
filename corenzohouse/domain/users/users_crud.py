from sqlalchemy.orm import Session
from ...model.users import Users
from sqlalchemy.future import select
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def users_get_list( db: Session, params: dict ):
    query = select(Users)

    # if params.get('key') is not None:
    #     query = query.where(Reviewers.key.ilike(f"%{params['key']}%"))
    # if params.get('min_date') is not None:
    #     query = query.where(Reviewers.create_date >= params['min_date'])
    # if params.get('max_date') is not None:
    #     query = query.where(Reviewers.create_date <= params['max_date'])
    # if params.get('oid') is not None:
    #     if not isinstance(params['oid'], list):  # 리스트 타입인지 확인
    #         query = query.where(Reviewers.order_id == params['oid'])
    #     else:
    #         query = query.where(Reviewers.order_id.in_(params['oid']))

    # if params.get('status') is not None:
    #     query = query.where(Orders.status == params['status'])
    
    print(f"Generated Query: {str(query)}")
    query= query.order_by(Users.id.desc())
    result= await db.execute(query)
    data = result.scalars().all()
    return data


# async def order_get_list(db: Session, key: str = None, min_date: int = None, max_date: int = None,
#                          tid: str = None, oid: str = None, sid: str = None, status: str = None):
#     query = select(Orders)

#     if key:
#         query = query.where(Orders.key.ilike(f"%{key}%"))  # 부분 검색 (대소문자 구분X)
#     if min_date:
#         query = query.where(Orders.create_date >= min_date)
#     if max_date:
#         query = query.where(Orders.create_date <= max_date)
#     if tid:
#         query = query.where(Orders.table_id == tid)
#     if oid:
#         query = query.where(Orders.order_id == oid)
#     if sid:
#         query = query.where(Orders.store_id == sid)
#     if status:
#         query = query.where(Orders.status == status)

    
#     print(f"Generated Query: {str(query)}")
#     query= query.order_by(Orders.id.desc())
#     result= await db.execute(query)
#     list = result.scalars().all()
#     return list