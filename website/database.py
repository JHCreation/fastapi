# import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from asyncio import current_task
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from .conn import DATABASE_URL_CONN, DATABASE_URL, DATABASE_URL_ASYNC, DATABASE_URL_ASYNC_CONN

# engine = create_engine(DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# def create_tables():
#     Base.metadata.create_all(bind=engine)
#     print("Tables created successfully")

class engineconn:

    def __init__(self):
        self.engine = create_engine(DATABASE_URL_CONN, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        return Session

    def connection(self):
        conn = self.engine.connect()
        return conn

db= engineconn()
# conn=  db.connection()
SessionLocal= db.sessionmaker()



# @contextlib.contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# ✅ 비동기 DB 엔진 생성
async_engine = create_async_engine(
    DATABASE_URL_ASYNC_CONN,
    pool_size=10,          # 연결 풀 크기 (적절히 조정)
    max_overflow=20,       # 초과 연결 허용 개수
    pool_recycle=1800,     # 30분 후 연결 새로고침 (3600 → 1800 권장)
    pool_pre_ping=True     # 죽은 연결 감지
)

# ✅ 세션팩토리 생성 (async_scoped_session 제거)
async_session_factory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False  # True면 commit 후 객체를 사용할 수 없음
)

# ✅ FastAPI 의존성 (각 요청마다 새로운 세션을 생성하고 종료)
async def get_async_db():
    async with async_session_factory() as db:  # ✅ `async with` 사용
        yield db  # 요청이 끝나면 세션 자동 반환됨

Base = declarative_base()


# async_engine= create_async_engine(DATABASE_URL_ASYNC_CONN, pool_recycle = 3600)
# async_session_factory = sessionmaker(bind=async_engine, class_=AsyncSession)
# session = async_scoped_session(
#     session_factory=async_session_factory,
#     scopefunc=current_task,
# )
# async def get_async_db():
#     db = session
#     try:
#         yield db
#     finally:
#         await db.close()

# Base = declarative_base()
