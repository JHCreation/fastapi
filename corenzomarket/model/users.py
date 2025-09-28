from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    userid = Column(String(100), unique=True, nullable=False)
    password = Column(String(80), nullable=True)
    email = Column(String(50), nullable=True)
    phone = Column(String(13), nullable=True)
    username = Column(String(50), nullable=True)
    usertype = Column(String(20), index=True, nullable=False)
    permission = Column(String(20), index=True, nullable=False)
    nickname = Column(String(50), nullable=True)
    org_name = Column(String(50), nullable=True)
    store_name = Column(String(50), nullable=True)
    domain = Column(String(50), nullable=True)
    modify_date = Column(DateTime, nullable=True)
    create_date = Column(DateTime, nullable=False)