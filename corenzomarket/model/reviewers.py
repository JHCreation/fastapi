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
    channel = Column(VARCHAR(128), nullable=True)
    gender = Column(VARCHAR(6), nullable=False)
    birthday = Column(VARCHAR(10), nullable=True)
    phone = Column(VARCHAR(20), nullable=False)
    email = Column(VARCHAR(50), nullable=True)
    link = Column(VARCHAR(1000), index=True, nullable=False)
    wish = Column(VARCHAR(128), nullable=True)
    service = Column(VARCHAR(255), nullable=True)
    msg = Column(VARCHAR(255), nullable=True)
    create_date = Column(DateTime, nullable=False)
    events = Column(VARCHAR(100), index=True, nullable=True)
    status = Column(VARCHAR(20), nullable=False, default='registered')
    memo = Column(VARCHAR(255), nullable=True)