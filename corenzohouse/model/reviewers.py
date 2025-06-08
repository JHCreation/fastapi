from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR, MEDIUMTEXT, INTEGER, JSON
from ..database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

class Reviewers(Base):
    __tablename__ = "reviewers"

    id = Column(Integer, primary_key=True)
    key = Column(VARCHAR(50), unique=True, nullable=False)
    name = Column(VARCHAR(50), index=True, nullable=False)
    channel = Column(MEDIUMTEXT, index=True, nullable=True)
    gender = Column(VARCHAR(6), index=True, nullable=False)
    birthday = Column(VARCHAR(10), nullable=True)
    phone = Column(VARCHAR(20), nullable=False)
    email = Column(VARCHAR(50), nullable=True)
    link = Column(LONGTEXT, index=True, nullable=False)
    wish_drink = Column(MEDIUMTEXT, index=True, nullable=False)
    msg = Column(MEDIUMTEXT, nullable=True)
    create_date = Column(DateTime, nullable=False)