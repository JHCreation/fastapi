from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR, MEDIUMTEXT, INTEGER
from .database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from .model import webpush, orders
# from .model import wine
print('model corenzo')
# class User(Base):
#     __tablename__ = "user"

#     id = Column(Integer, primary_key=True)
#     userid = Column(String(100), unique=True, nullable=False)
#     password = Column(String(500), nullable=True)
#     email = Column(String(50), nullable=False)
#     phone = Column(String(13), nullable=False)
#     username = Column(String(50), nullable=True)
#     usertype = Column(String(20), index=True, nullable=False)
#     permission = Column(String(20), index=True, nullable=False)
#     nickname = Column(String(100), nullable=True)
#     modify_date = Column(DateTime, nullable=False)
#     create_date = Column(DateTime, nullable=False)
#     sns_type = Column(String(50), index=True, nullable=False)
#     sns_id = Column(String(50), unique=True, nullable=False)
#     sns_name = Column(String(50), nullable=True)
#     sns_gender = Column(String(10), nullable=True)
#     sns_age = Column(String(10), nullable=True)
#     sns_birthyear = Column(String(10), nullable=True)
#     sns_birthday = Column(String(10), nullable=True)
#     sns_connect_date = Column(String(50), nullable=True)