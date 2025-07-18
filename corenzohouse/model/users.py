from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR, MEDIUMTEXT, INTEGER, JSON
from ..database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

# class Users(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(VARCHAR(50), unique=True, nullable=False)
#     name = Column(VARCHAR(50), index=True, nullable=False)
#     channel = Column(MEDIUMTEXT, index=True, nullable=True)
#     gender = Column(VARCHAR(6), index=True, nullable=False)
#     birthday = Column(VARCHAR(10), nullable=True)
#     phone = Column(VARCHAR(20), nullable=False)
#     email = Column(VARCHAR(50), nullable=True)
#     msg = Column(MEDIUMTEXT, nullable=True)
#     modify_date = Column(DateTime, nullable=False)
#     create_date = Column(DateTime, nullable=False)


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
    orgname = Column(String(50), nullable=True)
    domain = Column(String(50), nullable=True)
    modify_date = Column(DateTime, nullable=True)
    create_date = Column(DateTime, nullable=False)