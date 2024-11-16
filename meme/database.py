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


async_engine= create_async_engine(DATABASE_URL_ASYNC_CONN, pool_recycle = 3600)
async_session_factory = sessionmaker(bind=async_engine, class_=AsyncSession)
session = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=current_task,
)
async def get_async_db():
    db = session
    try:
        yield db
    finally:
        await db.close()

Base = declarative_base()
