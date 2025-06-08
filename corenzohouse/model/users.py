from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR, MEDIUMTEXT, INTEGER, JSON
from ..database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(VARCHAR(50), unique=True, nullable=False)
    name = Column(VARCHAR(50), index=True, nullable=False)
    channel = Column(MEDIUMTEXT, index=True, nullable=True)
    gender = Column(VARCHAR(6), index=True, nullable=False)
    birthday = Column(VARCHAR(10), nullable=True)
    phone = Column(VARCHAR(20), nullable=False)
    email = Column(VARCHAR(50), nullable=True)
    msg = Column(MEDIUMTEXT, nullable=True)
    modify_date = Column(DateTime, nullable=False)
    create_date = Column(DateTime, nullable=False)