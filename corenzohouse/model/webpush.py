from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, VARCHAR, MEDIUMTEXT, INTEGER
from ..database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

class WebPush(Base):
    __tablename__ = "webpush"

    id = Column(Integer, primary_key=True)
    key = Column(VARCHAR(50), unique=True, nullable=False)
    subscription = Column(MEDIUMTEXT, nullable=True)
    endpoint = Column(VARCHAR(300), index=True, nullable=True)
    status = Column(VARCHAR(10), index=True, nullable=True)
    modify_date = Column(DateTime, nullable=False)
    create_date = Column(DateTime, nullable=False)

class WebPushLog(Base):
    __tablename__ = "webpush_log"

    id = Column(Integer, primary_key=True)
    log = Column(MEDIUMTEXT, nullable=True)
    create_date = Column(DateTime, nullable=False)