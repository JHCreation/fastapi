from sqlalchemy.orm import Session
from ...model.orders import Orders
from sqlalchemy.future import select


async def order_get_list(db: Session, key: str = None, min_date: int = None, max_date: int = None):
    query = select(Orders)
    print('min_date', min_date)
    print('max_date', max_date)
    if key:
        query = query.where(Orders.key.ilike(f"%{key}%"))  # 부분 검색 (대소문자 구분X)
    if min_date:
        query = query.where(Orders.create_date >= min_date)
    if max_date:
        query = query.where(Orders.create_date <= max_date)
    
    print(f"Generated Query: {str(query)}")
    query= query.order_by(Orders.id.desc())
    result= await db.execute(query)
    list = result.scalars().all()
    return list